"""
Fallback workout generator for when AI models fail.
Generates rule-based workout plans based on user profile.
"""
import uuid
from datetime import date
from app.models.user import UserProfile
from app.models.workout import WorkoutPlan, WorkoutDay, Exercise, ExerciseType
from app.services.workout_library import EXERCISE_LIBRARY


class FallbackWorkoutGenerator:
    """Generate workout plans using rule-based logic"""

    def __init__(self):
        self.exercise_library = EXERCISE_LIBRARY

    def generate_workout_plan(self, user_profile: UserProfile) -> WorkoutPlan:
        """Generate a personalized workout plan based on user profile"""

        #Determine workout structure based on days per week
        workout_focuses = self._get_workout_focuses(user_profile.days_per_week)

        #Create weekly schedule
        weekly_schedule = []
        for day_num in range(user_profile.days_per_week):
            focus = workout_focuses[day_num]
            exercises = self._get_exercises_for_focus(focus, user_profile)

            workout_day = WorkoutDay(
                day=day_num + 1,
                focus=focus,
                exercises=exercises,
                total_duration=user_profile.workout_duration or 40
            )
            weekly_schedule.append(workout_day)

        return WorkoutPlan(
            id=str(uuid.uuid4()),
            user_profile=user_profile,
            generated_date=date.today(),
            duration_weeks=1,
            weekly_schedule=weekly_schedule
        )

    def _get_workout_focuses(self, days_per_week: int) -> list:
        """Determine workout focuses based on training frequency"""

        if days_per_week <= 2:
            return ["Full Body", "Full Body"][:days_per_week]
        elif days_per_week == 3:
            return ["Upper Body", "Lower Body", "Full Body"]
        elif days_per_week == 4:
            return ["Upper Body", "Lower Body", "Core & Cardio", "Full Body"]
        elif days_per_week == 5:
            return ["Upper Body", "Lower Body", "Core & Conditioning", "Full Body", "Cardio & Flexibility"]
        elif days_per_week == 6:
            return ["Upper Body Push", "Lower Body", "Core", "Upper Body Pull", "Legs & Cardio", "Full Body"]
        else:
            return ["Upper Body Push", "Lower Body", "Core & Cardio", "Upper Body Pull", "Legs", "Full Body", "Active Recovery"]

    def _get_exercises_for_focus(self, focus: str, profile: UserProfile) -> list:
        """Get appropriate exercises based on workout focus and user profile"""

        #Filter exercises based on available equipment
        available_equipment = set(profile.available_equipment) if profile.available_equipment else {"bodyweight"}

        #Adjust difficulty based on fitness level
        reps_multiplier = self._get_reps_multiplier(profile.fitness_level)
        sets_multiplier = self._get_sets_multiplier(profile.fitness_level)

        exercises = []

        if "Upper Body" in focus:
            exercises = self._get_upper_body_exercises(focus, available_equipment, reps_multiplier, sets_multiplier)
        elif "Lower Body" in focus or "Legs" in focus:
            exercises = self._get_lower_body_exercises(available_equipment, reps_multiplier, sets_multiplier)
        elif "Core" in focus:
            exercises = self._get_core_exercises(available_equipment, reps_multiplier, sets_multiplier)
        elif "Cardio" in focus or "Conditioning" in focus:
            exercises = self._get_cardio_exercises(available_equipment, reps_multiplier, sets_multiplier)
        elif "Full Body" in focus:
            exercises = self._get_full_body_exercises(available_equipment, reps_multiplier, sets_multiplier)
        elif "Active Recovery" in focus or "Flexibility" in focus:
            exercises = self._get_recovery_exercises(reps_multiplier, sets_multiplier)
        else:
            exercises = self._get_full_body_exercises(available_equipment, reps_multiplier, sets_multiplier)

        return exercises

    def _get_reps_multiplier(self, fitness_level: str) -> float:
        """Get rep count multiplier based on fitness level"""
        multipliers = {
            "beginner": 0.8,
            "intermediate": 1.0,
            "advanced": 1.2
        }
        return multipliers.get(fitness_level, 1.0)

    def _get_sets_multiplier(self, fitness_level: str) -> int:
        """Get set count based on fitness level"""
        sets = {
            "beginner": 2,
            "intermediate": 3,
            "advanced": 4
        }
        return sets.get(fitness_level, 3)

    def _filter_by_equipment(self, exercises: list, available_equipment: set) -> list:
        """Filter exercises that match available equipment"""
        filtered = []
        for exercise in exercises:
            if exercise['equipment'] == 'none' or exercise['equipment'] in available_equipment:
                filtered.append(exercise)
        return filtered

    def _get_upper_body_exercises(self, focus: str, equipment: set, reps_mult: float, sets: int) -> list:
        """Get upper body exercises"""
        exercises = []

        #Get available exercises
        strength_exercises = self._filter_by_equipment(self.exercise_library.get('strength', []), equipment)

        if "Push" in focus:
            #Prioritize pushing movements
            push_exercises = [e for e in strength_exercises if any(word in e['name'].lower() for word in ['push', 'press', 'dip'])]
            exercises = push_exercises[:3] if push_exercises else strength_exercises[:3]
        elif "Pull" in focus:
            #Prioritize pulling movements
            pull_exercises = [e for e in strength_exercises if any(word in e['name'].lower() for word in ['pull', 'row', 'chin'])]
            exercises = pull_exercises[:3] if pull_exercises else strength_exercises[:3]
        else:
            #Mixed upper body
            exercises = strength_exercises[:4]

        return self._create_exercise_objects(exercises, ExerciseType.STRENGTH, int(12 * reps_mult), sets, 60)

    def _get_lower_body_exercises(self, equipment: set, reps_mult: float, sets: int) -> list:
        """Get lower body exercises"""
        strength_exercises = self._filter_by_equipment(self.exercise_library.get('strength', []), equipment)
        leg_exercises = [e for e in strength_exercises if any(word in e['name'].lower() for word in ['squat', 'lunge', 'leg', 'glute', 'calf'])]

        selected = leg_exercises[:4] if leg_exercises else strength_exercises[:4]
        return self._create_exercise_objects(selected, ExerciseType.STRENGTH, int(15 * reps_mult), sets, 60)

    def _get_core_exercises(self, equipment: set, reps_mult: float, sets: int) -> list:
        """Get core exercises"""
        core_exercises = self._filter_by_equipment(self.exercise_library.get('core', []), equipment)
        selected = core_exercises[:5] if core_exercises else []

        #Core exercises often use duration instead of reps
        return [
            Exercise(
                name=ex['name'],
                type=ExerciseType.CORE,
                sets=sets,
                duration=int(30 * reps_mult) if 'plank' in ex['name'].lower() else None,
                reps=int(15 * reps_mult) if 'plank' not in ex['name'].lower() else None,
                rest=30
            )
            for ex in selected
        ]

    def _get_cardio_exercises(self, equipment: set, reps_mult: float, sets: int) -> list:
        """Get cardio exercises"""
        cardio_exercises = self._filter_by_equipment(self.exercise_library.get('cardio', []), equipment)
        selected = cardio_exercises[:4] if cardio_exercises else []

        return [
            Exercise(
                name=ex['name'],
                type=ExerciseType.CARDIO,
                sets=sets,
                duration=int(45 * reps_mult),
                rest=30
            )
            for ex in selected
        ]

    def _get_full_body_exercises(self, equipment: set, reps_mult: float, sets: int) -> list:
        """Get full body workout exercises"""
        exercises = []

        #Mix of strength, core, and cardio
        strength = self._filter_by_equipment(self.exercise_library.get('strength', []), equipment)[:2]
        core = self._filter_by_equipment(self.exercise_library.get('core', []), equipment)[:2]
        cardio = self._filter_by_equipment(self.exercise_library.get('cardio', []), equipment)[:1]

        #Add strength exercises
        exercises.extend(self._create_exercise_objects(strength, ExerciseType.STRENGTH, int(12 * reps_mult), sets, 60))

        #Add core exercises
        for ex in core:
            exercises.append(Exercise(
                name=ex['name'],
                type=ExerciseType.CORE,
                sets=sets - 1,
                duration=int(30 * reps_mult) if 'plank' in ex['name'].lower() else None,
                reps=int(12 * reps_mult) if 'plank' not in ex['name'].lower() else None,
                rest=30
            ))

        #Add cardio exercise
        for ex in cardio:
            exercises.append(Exercise(
                name=ex['name'],
                type=ExerciseType.CARDIO,
                sets=2,
                duration=int(30 * reps_mult),
                rest=30
            ))

        return exercises

    def _get_recovery_exercises(self, reps_mult: float, sets: int) -> list:
        """Get active recovery/flexibility exercises"""
        flexibility = self.exercise_library.get('flexibility', [])
        selected = flexibility[:5] if flexibility else []

        return [
            Exercise(
                name=ex['name'],
                type=ExerciseType.FLEXIBILITY,
                sets=2,
                duration=int(30 * reps_mult),
                rest=15
            )
            for ex in selected
        ]

    def _create_exercise_objects(self, exercise_dicts: list, exercise_type: ExerciseType, reps: int, sets: int, rest: int) -> list:
        """Create Exercise objects from exercise dictionaries"""
        return [
            Exercise(
                name=ex['name'],
                type=exercise_type,
                sets=sets,
                reps=reps,
                rest=rest
            )
            for ex in exercise_dicts
        ]
