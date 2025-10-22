import os
import json
import requests
from typing import Dict, Any
from datetime import date
import uuid
from dotenv import load_dotenv

#Load environment variables
load_dotenv()

from app.models.user import UserProfile
from app.models.workout import WorkoutPlan, WorkoutDay, WorkoutWeek, Exercise, ExerciseType
from app.services.workout_library import EXERCISE_LIBRARY
from app.services.fallback_workout_generator import FallbackWorkoutGenerator


class HuggingFaceWorkoutGenerator:
    def __init__(self):
        self.fallback_generator = FallbackWorkoutGenerator()
        #Use the correct Chat Completions API endpoint
        self.api_url = "https://router.huggingface.co/v1/chat/completions"
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")

        #List of models to try in order
        self.models = [
            "Qwen/Qwen3-Next-80B-A3B-Instruct:novita",
            "deepseek-ai/DeepSeek-R1:novita",
            "deepseek-ai/DeepSeek-V3:nebius",
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B:featherless-ai"
        ]

        if self.api_token:
            self.headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            print("Hugging Face API token loaded")
            print("Using Chat Completions API")
        else:
            self.headers = {}
            print("WARNING: Hugging Face API token not found")
    
    def generate_workout_plan(self, user_profile: UserProfile) -> WorkoutPlan:
        if self.api_token:
            try:
                print("Attempting AI workout generation...")
                return self._generate_with_huggingface(user_profile)
            except Exception as e:
                print(f"ERROR: AI generation failed: {e}")
                print("Using fallback workout generator...")
                return self.fallback_generator.generate_workout_plan(user_profile)
        else:
            print("No API token found. Using fallback workout generator...")
            return self.fallback_generator.generate_workout_plan(user_profile)
    
    def _generate_with_huggingface(self, user_profile: UserProfile) -> WorkoutPlan:
        prompt = self._build_prompt(user_profile)

        last_error = None

        for i, model in enumerate(self.models):
            print(f"Trying model {i+1}/{len(self.models)}: {model}")

            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": model,
                "max_tokens": 1000,
                "temperature": 0.7
            }

            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )

                print(f"Response status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    print(f"Model {model} succeeded!")
                    workout_data = self._parse_ai_response(result, user_profile)
                    return self._create_workout_plan(user_profile, workout_data)
                else:
                    error_msg = f"API error {response.status_code}: {response.text}"
                    print(f"Model {model} failed: {error_msg}")
                    last_error = error_msg
                    continue

            except requests.exceptions.Timeout:
                error_msg = f"Model {model} timeout"
                print(f"ERROR: {error_msg}")
                last_error = error_msg
                continue
            except Exception as e:
                error_msg = f"Model {model} error: {e}"
                print(f"ERROR: {error_msg}")
                last_error = error_msg
                continue

        #If all models failed, raise the last error
        print(f"All {len(self.models)} models failed. Using fallback workout.")
        raise Exception(f"All models failed. Last error: {last_error}")
    
    def _build_prompt(self, profile: UserProfile) -> str:
        #Build the available exercises list from the library
        available_exercises = "\n\nAVAILABLE EXERCISES (You MUST only choose from these):\n"

        for exercise_type, exercises in EXERCISE_LIBRARY.items():
            available_exercises += f"\n{exercise_type.upper()} EXERCISES:\n"
            for exercise in exercises:
                equipment_text = f" (requires: {exercise['equipment']})" if exercise['equipment'] != 'none' else ""
                available_exercises += f"- {exercise['name']}{equipment_text}\n"

        return f"""Create a personalized workout plan in JSON format.

User Profile:
- Age: {profile.age}
- Weight: {profile.weight}kg
- Height: {profile.height}cm
- Fitness Level: {profile.fitness_level}
- Goal: {profile.goal}
- Available Equipment: {', '.join(profile.available_equipment)}
- Workout Duration: {profile.workout_duration} minutes per session
- Days per Week: {profile.days_per_week}

{available_exercises}

Please generate a {profile.days_per_week}-day workout plan. Return ONLY valid JSON in this exact format:

IMPORTANT:
1. Exercise type must be one of: "strength", "cardio", "flexibility", "warmup", "cooldown", "core"
2. You MUST ONLY choose exercise names from the AVAILABLE EXERCISES list above
3. Consider the user's available equipment when selecting exercises

{{
  "weekly_schedule": [
    {{
      "day": 1,
      "focus": "Upper Body",
      "exercises": [
        {{
          "name": "Exercise Name",
          "type": "strength",
          "sets": 3,
          "reps": 12,
          "rest": 60
        }}
      ],
      "total_duration": {profile.workout_duration}
    }},
    {{
      "day": 2,
      "focus": "Lower Body",
      "exercises": [
        {{
          "name": "Different Exercise Name",
          "type": "strength",
          "sets": 3,
          "reps": 15,
          "rest": 60
        }}
      ],
      "total_duration": {profile.workout_duration}
    }}
  ]
}}

Generate all {profile.days_per_week} days with different focuses and exercises for variety.

CRITICAL: Return ONLY valid JSON on a single line with NO newlines, NO formatting, NO other text. Example format: {{"weekly_schedule":[{{"day":1,"focus":"Upper Body","exercises":[{{"name":"Push-ups","type":"strength","sets":3,"reps":12,"rest":60}}],"total_duration":40}}]}}"""
    
    def _parse_ai_response(self, response_data: Dict, user_profile: UserProfile) -> Dict[str, Any]:
        """Parse the Chat Completions API response"""
        print(f"Parsing response...")

        try:
            #Extract the message content from the response
            message_content = response_data["choices"][0]["message"]["content"]

            #Try to extract JSON from the response
            workout_data = self._extract_json_from_text(message_content)

            if workout_data:
                return workout_data
            else:
                #If JSON extraction fails, return default workout data
                print("JSON extraction failed, using default workout data")
                return self._get_default_workout_data()

        except Exception as e:
            print(f"ERROR: Error parsing AI response: {e}")
            return self._get_default_workout_data()
    
    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Extract JSON from text response"""
        json_str = ""
        try:
            #Clean the text and find JSON
            text = text.strip()

            #Look for JSON object
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                print(f"Extracted JSON length: {len(json_str)} characters")

                #Try to fix common JSON issues
                json_str = self._fix_common_json_issues(json_str)

                #Parse the JSON first
                parsed_json = json.loads(json_str)

                #Save formatted JSON to a file for debugging
                with open("debug_workout.json", "w") as f:
                    json.dump(parsed_json, f, indent=2)
                print("Saved formatted JSON to debug_workout.json for inspection")

                #Print the complete formatted workout
                print("AI Generated Workout (complete):")
                print(json.dumps(parsed_json, indent=2))

                return parsed_json
        except json.JSONDecodeError as e:
            print(f"ERROR: JSON decode error: {e}")
            print(f"Problematic JSON around position {e.pos}:")
            if hasattr(e, 'pos') and e.pos and json_str:
                start = max(0, e.pos - 100)
                end = min(len(json_str), e.pos + 100)
                print(f"...{json_str[start:end]}...")

                #Try to auto-fix the JSON
                fixed_json = self._attempt_json_fix(json_str, e.pos)
                if fixed_json:
                    try:
                        return json.loads(fixed_json)
                    except:
                        print("Auto-fix failed, falling back to default")

        return None

    def _fix_common_json_issues(self, json_str: str) -> str:
        """Fix common JSON formatting issues"""
        import re

        #Remove actual newlines and tabs (replace with spaces)
        json_str = json_str.replace('\n', ' ').replace('\t', ' ')

        #Remove extra whitespace
        json_str = re.sub(r'\s+', ' ', json_str)

        #Remove trailing commas before closing brackets/braces
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)

        #Fix missing commas between objects/arrays
        json_str = re.sub(r'}\s*{', '},{', json_str)
        json_str = re.sub(r']\s*\[', '],[', json_str)
        json_str = re.sub(r'}\s*\[', '},[', json_str)
        json_str = re.sub(r']\s*{', '],{', json_str)

        #Fix common quote issues (but be careful not to break valid escapes)
        json_str = re.sub(r'([^\\])"([^":,}\]]+)"([^:])', r'\1"\2"\3', json_str)

        return json_str.strip()

    def _attempt_json_fix(self, json_str: str, error_pos: int) -> str:
        """Attempt to automatically fix JSON parsing errors"""
        import re

        try:
            #Check if it's a missing comma issue
            if error_pos < len(json_str):
                char_at_pos = json_str[error_pos]
                char_before = json_str[error_pos - 1] if error_pos > 0 else ''

                #If we're expecting a comma and found a quote or brace
                if char_at_pos in ['"', '{'] and char_before in ['}', ']']:
                    print(f"Attempting to fix missing comma at position {error_pos}")
                    fixed_json = json_str[:error_pos] + ',' + json_str[error_pos:]
                    return fixed_json

                #Check for unescaped quotes in strings
                if char_at_pos == '"' and char_before != '\\':
                    #Look backwards to see if we're inside a string value
                    context_start = max(0, error_pos - 50)
                    context = json_str[context_start:error_pos + 50]
                    if context.count('"') % 2 == 1:  # Odd number means we're inside a string
                        print(f"Attempting to escape quote at position {error_pos}")
                        fixed_json = json_str[:error_pos] + '\\"' + json_str[error_pos + 1:]
                        return fixed_json

            #Try to fix trailing commas
            fixed_json = re.sub(r',(\s*[}\]])', r'\1', json_str)
            if fixed_json != json_str:
                print("Fixed trailing commas")
                return fixed_json

        except Exception as e:
            print(f"JSON auto-fix error: {e}")

        return None

    def _get_default_workout_data(self) -> Dict[str, Any]:
        """Generate a simple default weekly workout structure"""
        weekly_schedule = []

        #Define workout focuses for variety
        focuses = ["Upper Body", "Lower Body", "Full Body", "Core & Cardio", "Strength"]

        #Create 5 days of workouts
        for day_num in range(1, 6):
            focus = focuses[(day_num - 1) % len(focuses)]
            weekly_schedule.append({
                "day": day_num,
                "focus": focus,
                "exercises": [
                    {
                        "name": "Push-ups",
                        "type": "strength",
                        "sets": 3,
                        "reps": 12,
                        "rest": 60
                    },
                    {
                        "name": "Squats",
                        "type": "strength",
                        "sets": 3,
                        "reps": 15,
                        "rest": 60
                    }
                ],
                "total_duration": 40
            })

        return {
            "weekly_schedule": weekly_schedule
        }
    
    def _create_workout_plan(self, user_profile: UserProfile, workout_data: Dict) -> WorkoutPlan:
        """Create WorkoutPlan from data"""

        #Parse the weekly schedule from the data
        weekly_schedule = []
        for day_data in workout_data.get("weekly_schedule", []):
            exercises = []
            for ex_data in day_data.get("exercises", []):
                exercise = Exercise(
                    name=ex_data.get("name", "Exercise"),
                    type=ExerciseType(ex_data.get("type", "strength")),
                    sets=ex_data.get("sets", 3),
                    reps=ex_data.get("reps", 10),
                    duration=ex_data.get("duration"),
                    rest=ex_data.get("rest", 60)
                )
                exercises.append(exercise)

            workout_day = WorkoutDay(
                day=day_data.get("day", 1),
                focus=day_data.get("focus", "Workout"),
                exercises=exercises,
                total_duration=day_data.get("total_duration", user_profile.workout_duration or 40)
            )
            weekly_schedule.append(workout_day)

        return WorkoutPlan(
            id=str(uuid.uuid4()),
            user_profile=user_profile,
            generated_date=date.today(),
            duration_weeks=1,
            weekly_schedule=weekly_schedule
        )


#For backward compatibility
AIWorkoutGenerator = HuggingFaceWorkoutGenerator