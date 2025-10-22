from typing import List
#Pre-defined exercise library
EXERCISE_LIBRARY = {
    "strength": [
        {
            "name": "Push-ups",
            "type": "strength",
            "equipment": "bodyweight",
            "muscle_groups": ["chest", "shoulders", "triceps"]
        },
        {
            "name": "Squats",
            "type": "strength",
            "equipment": "bodyweight",
            "muscle_groups": ["quadriceps", "glutes", "hamstrings"]
        },
        {
            "name": "Pull-ups",
            "type": "strength",
            "equipment": "pull-up bar",
            "muscle_groups": ["lats", "biceps", "rhomboids"]
        },
        {
            "name": "Lunges",
            "type": "strength",
            "equipment": "bodyweight",
            "muscle_groups": ["quadriceps", "glutes", "hamstrings"]
        },
        {
            "name": "Planks",
            "type": "strength",
            "equipment": "bodyweight",
            "muscle_groups": ["core", "abs"]
        },
        {
            "name": "Sit-ups",
            "type": "strength",
            "equipment": "bodyweight",
            "muscle_groups": ["abs", "core"]
        },
        {
            "name": "Burpees",
            "type": "strength",
            "equipment": "bodyweight",
            "muscle_groups": ["full body"]
        },
        {
            "name": "Jumping Jacks",
            "type": "strength",
            "equipment": "bodyweight",
            "muscle_groups": ["legs", "shoulders"]
        }
    ],
    "cardio": [
        {
            "name": "Running",
            "type": "cardio",
            "equipment": "none"
        },
        {
            "name": "Walking",
            "type": "cardio",
            "equipment": "none"
        },
        {
            "name": "Cycling",
            "type": "cardio",
            "equipment": "bicycle"
        },
        {
            "name": "Swimming",
            "type": "cardio",
            "equipment": "pool"
        },
        {
            "name": "Jump Rope",
            "type": "cardio",
            "equipment": "jump rope"
        },
        {
            "name": "Jogging",
            "type": "cardio",
            "equipment": "none"
        }
    ],
    "flexibility": [
        {
            "name": "Hamstring Stretch",
            "type": "flexibility",
            "equipment": "none",
            "muscle_groups": ["hamstrings"]
        },
        {
            "name": "Shoulder Stretch",
            "type": "flexibility",
            "equipment": "none",
            "muscle_groups": ["shoulders"]
        },
        {
            "name": "Calf Stretch",
            "type": "flexibility",
            "equipment": "none",
            "muscle_groups": ["calves"]
        },
        {
            "name": "Hip Flexor Stretch",
            "type": "flexibility",
            "equipment": "none",
            "muscle_groups": ["hip flexors"]
        },
        {
            "name": "Quad Stretch",
            "type": "flexibility",
            "equipment": "none",
            "muscle_groups": ["quadriceps"]
        },
        {
            "name": "Tricep Stretch",
            "type": "flexibility",
            "equipment": "none",
            "muscle_groups": ["triceps"]
        }
    ],
    "warmup": [
        {
            "name": "Arm Circles",
            "type": "warmup",
            "equipment": "none",
            "muscle_groups": ["shoulders", "arms"]
        },
        {
            "name": "Leg Swings",
            "type": "warmup",
            "equipment": "none",
            "muscle_groups": ["legs", "hips"]
        },
        {
            "name": "Light Jogging in Place",
            "type": "warmup",
            "equipment": "none",
            "muscle_groups": ["legs", "cardiovascular"]
        },
        {
            "name": "High Knees",
            "type": "warmup",
            "equipment": "none",
            "muscle_groups": ["legs", "core"]
        },
        {
            "name": "Butt Kicks",
            "type": "warmup",
            "equipment": "none",
            "muscle_groups": ["legs", "glutes"]
        },
        {
            "name": "Neck Rolls",
            "type": "warmup",
            "equipment": "none",
            "muscle_groups": ["neck"]
        }
    ],
    "cooldown": [
        {
            "name": "Walking",
            "type": "cooldown",
            "equipment": "none",
            "muscle_groups": ["legs"]
        },
        {
            "name": "Deep Breathing",
            "type": "cooldown",
            "equipment": "none",
            "muscle_groups": ["respiratory"]
        },
        {
            "name": "Gentle Stretching",
            "type": "cooldown",
            "equipment": "none",
            "muscle_groups": ["full body"]
        },
        {
            "name": "Child's Pose",
            "type": "cooldown",
            "equipment": "none",
            "muscle_groups": ["back", "hips"]
        },
        {
            "name": "Seated Forward Bend",
            "type": "cooldown",
            "equipment": "none",
            "muscle_groups": ["hamstrings", "back"]
        }
    ],
    "core": [
        {
            "name": "Crunches",
            "type": "core",
            "equipment": "bodyweight",
            "muscle_groups": ["abs"]
        },
        {
            "name": "Planks",
            "type": "core",
            "equipment": "bodyweight",
            "muscle_groups": ["core", "abs"]
        },
        {
            "name": "Bicycle Crunches",
            "type": "core",
            "equipment": "bodyweight",
            "muscle_groups": ["abs", "obliques"]
        },
        {
            "name": "Russian Twists",
            "type": "core",
            "equipment": "bodyweight",
            "muscle_groups": ["obliques", "core"]
        },
        {
            "name": "Mountain Climbers",
            "type": "core",
            "equipment": "bodyweight",
            "muscle_groups": ["core", "shoulders"]
        },
        {
            "name": "Dead Bug",
            "type": "core",
            "equipment": "bodyweight",
            "muscle_groups": ["core", "abs"]
        }
    ]
}

class WorkoutLibrary:
    def get_exercises_by_type(self, exercise_type: str, equipment: List[str] = None):
        exercises = EXERCISE_LIBRARY.get(exercise_type, [])
        if equipment:
            return [ex for ex in exercises if ex.get('equipment') in equipment or ex.get('equipment') == 'bodyweight']
        return exercises