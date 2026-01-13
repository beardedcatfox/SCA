import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from cats.models import Cat
from missions.models import Mission, Target
from cats.validators import validate_breed


class Command(BaseCommand):
    help = 'Initial test data (cats, missions, targets)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to seed data...')

        # Delete old data !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.stdout.write('Cleaning old data...')
        Target.objects.all().delete()
        Mission.objects.all().delete()
        Cat.objects.all().delete()

        self.stdout.write('Creating cats...')
        cats = self.create_cats()

        self.stdout.write('Creating missions with targets...')
        self.create_missions_with_targets(cats)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
        self.stdout.write(f'Created {Cat.objects.count()} cats')
        self.stdout.write(f'Created {Mission.objects.count()} missions')
        self.stdout.write(f'Created {Target.objects.count()} targets')

    def get_breeds_from_api(self):
        try:
            import requests
            response = requests.get('https://api.thecatapi.com/v1/breeds', timeout=3)
            if response.status_code == 200:
                breeds_data = response.json()
                return [breed['name'] for breed in breeds_data if 'name' in breed]
        except:
            pass

        return [
            'Abyssinian', 'Aegean', 'American Bobtail', 'American Curl',
            'American Shorthair', 'American Wirehair', 'Arabian Mau',
            'Australian Mist', 'Balinese', 'Bengal', 'Birman', 'Bombay',
            'British Shorthair', 'Burmese', 'Burmilla', 'Chartreux',
            'Cornish Rex', 'Devon Rex', 'Egyptian Mau', 'Exotic Shorthair',
            'Himalayan', 'Japanese Bobtail', 'Korat', 'LaPerm', 'Maine Coon',
            'Manx', 'Norwegian Forest Cat', 'Ocicat', 'Oriental', 'Persian',
            'Ragdoll', 'Russian Blue', 'Scottish Fold', 'Siamese', 'Siberian',
            'Singapura', 'Somali', 'Sphynx', 'Tonkinese', 'Turkish Angora'
        ]

    def create_cats(self):
        breeds = self.get_breeds_from_api()

        cats_data = [
            {
                'name': 'Shadow',
                'years_of_experience': 5,
                'breed': random.choice(breeds),
                'salary': 2500.00,
                'is_available': True
            },
            {
                'name': 'Whiskers',
                'years_of_experience': 3,
                'breed': random.choice(breeds),
                'salary': 1800.00,
                'is_available': True
            },
            {
                'name': 'Mittens',
                'years_of_experience': 1,
                'breed': random.choice(breeds),
                'salary': 1200.00,
                'is_available': True
            },
            {
                'name': 'Midnight',
                'years_of_experience': 7,
                'breed': random.choice(breeds),
                'salary': 3000.00,
                'is_available': True
            },
            {
                'name': 'Luna',
                'years_of_experience': 2,
                'breed': random.choice(breeds),
                'salary': 1500.00,
                'is_available': True
            }
        ]

        cats = []
        for cat_data in cats_data:
            cat = Cat.objects.create(**cat_data)
            cats.append(cat)
            self.stdout.write(f'  Created cat: {cat.name} ({cat.breed})')

        return cats

    def create_missions_with_targets(self, cats):
        mission1 = Mission.objects.create(cat=cats[0])
        cats[0].is_available = False
        cats[0].save()

        Target.objects.create(
            mission=mission1,
            name='Dr. Evil',
            country='Germany',
            notes='Suspected weapons dealer. Known to visit Berlin every Friday.',
            is_completed=False
        )
        self.stdout.write(f'  Created Mission 1 with 1 target, assigned to {cats[0].name}')

        mission2 = Mission.objects.create(cat=cats[1])
        cats[1].is_available = False
        cats[1].save()

        Target.objects.create(
            mission=mission2,
            name='The Banker',
            country='Switzerland',
            notes='Money laundering through crypto exchanges.',
            is_completed=False
        )

        Target.objects.create(
            mission=mission2,
            name='The Diplomat',
            country='France',
            notes='Suspected double agent. Meeting with unknown contacts.',
            is_completed=True
        )
        self.stdout.write(f'  Created Mission 2 with 2 targets, assigned to {cats[1].name}')

        mission3 = Mission.objects.create(cat=cats[2])
        cats[2].is_available = False
        cats[2].save()

        Target.objects.create(
            mission=mission3,
            name='Agent X',
            country='Iran',
            notes='Nuclear scientist. Works at secret facility.',
            is_completed=False
        )

        Target.objects.create(
            mission=mission3,
            name='The Hacker',
            country='Ukraine',
            notes='Cyber attacks on government systems. Uses VPNs extensively.',
            is_completed=False
        )

        Target.objects.create(
            mission=mission3,
            name='The Informant',
            country='Poland',
            notes='Provides information to multiple agencies. Unreliable.',
            is_completed=False
        )
        self.stdout.write(f'  Created Mission 3 with 3 targets, assigned to {cats[2].name}')

        mission4 = Mission.objects.create(cat=None)

        Target.objects.create(
            mission=mission4,
            name='The Collector',
            country='Japan',
            notes='Traffics rare artifacts. Base in Kyoto.',
            is_completed=False
        )

        Target.objects.create(
            mission=mission4,
            name='The Chemist',
            country='Netherlands',
            notes='Produces illegal substances. Lab in Rotterdam port.',
            is_completed=False
        )
        self.stdout.write(f'  Created Mission 4 with 2 targets, unassigned (no cat)')


        if random.choice([True, False]):
            mission1.is_completed = True
            mission1.save()
            cats[0].is_available = True
            cats[0].save()
            self.stdout.write(f'  Mission 1 marked as completed')
