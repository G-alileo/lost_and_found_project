from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from items.models import Category
from reports.models import Report
from matches.models import Match
from notifications.models import Notification

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
        
        # Create categories
        categories_data = [
            'Electronics',
            'Clothing',
            'Books',
            'Accessories',
            'Sports Equipment',
            'Personal Items'
        ]
        
        categories = []
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'created_by': admin_user}
            )
            categories.append(category)
        
        # Create sample reports
        reports_data = [
            {
                'title': 'Lost iPhone 14 Pro',
                'description': 'Black iPhone 14 Pro with blue case. Lost in the library.',
                'report_type': 'lost',
                'location': 'Main Library - 2nd Floor',
                'date_lost_found': date.today() - timedelta(days=2)
            },
            {
                'title': 'Found Laptop Charger',
                'description': 'MacBook charger found in Computer Science building.',
                'report_type': 'found',
                'location': 'CS Building - Room 201',
                'date_lost_found': date.today() - timedelta(days=1)
            },
            {
                'title': 'Lost Blue Backpack',
                'description': 'Navy blue Jansport backpack with laptop inside.',
                'report_type': 'lost',
                'location': 'Student Union',
                'date_lost_found': date.today() - timedelta(days=3)
            },
            {
                'title': 'Found Keys',
                'description': 'Set of keys with Toyota keychain.',
                'report_type': 'found',
                'location': 'Parking Lot B',
                'date_lost_found': date.today()
            },
            {
                'title': 'Lost Textbook',
                'description': 'Calculus textbook, 3rd edition.',
                'report_type': 'lost',
                'location': 'Math Building',
                'date_lost_found': date.today() - timedelta(days=5)
            }
        ]
        
        reports = []
        for report_data in reports_data:
            report, created = Report.objects.get_or_create(
                title=report_data['title'],
                defaults={
                    'description': report_data['description'],
                    'category': categories[0],  # Electronics for now
                    'report_type': report_data['report_type'],
                    'location': report_data['location'],
                    'date_lost_found': report_data['date_lost_found'],
                    'reported_by': admin_user
                }
            )
            reports.append(report)
        
        # Create sample matches
        lost_reports = [r for r in reports if r.report_type == 'lost']
        found_reports = [r for r in reports if r.report_type == 'found']
        
        if lost_reports and found_reports:
            # Create a potential match
            match, created = Match.objects.get_or_create(
                lost_report=lost_reports[0],
                found_report=found_reports[0],
                defaults={
                    'confidence_score': 0.85,
                    'status': 'pending'
                }
            )
            
            if created:
                # Create notification for the match
                Notification.objects.get_or_create(
                    user=admin_user,
                    message=f'Potential match found for your report "{lost_reports[0].title}"',
                    defaults={'related_match': match}
                )
        
        # Create some additional notifications
        notification_messages = [
            'Your report has been published and is now searchable.',
            'New items matching your criteria have been reported.',
            'Your report will expire in 30 days. Please update if still relevant.'
        ]
        
        for msg in notification_messages:
            Notification.objects.get_or_create(
                user=admin_user,
                message=msg,
                defaults={'is_read': False}
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {len(categories)} categories\n'
                f'- {len(reports)} reports\n'
                f'- {Match.objects.count()} matches\n'
                f'- {Notification.objects.count()} notifications'
            )
        )
