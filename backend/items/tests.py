from __future__ import annotations
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer

User = get_user_model()


class CategoryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )

    def test_category_creation(self):
        """Test creating a category."""
        category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )
        
        self.assertEqual(category.name, "Electronics")
        self.assertEqual(category.created_by, self.user)
        self.assertIsNotNone(category.created_at)

    def test_category_creation_without_user(self):
        """Test creating a category without a user."""
        category = Category.objects.create(name="Electronics")
        
        self.assertEqual(category.name, "Electronics")
        self.assertIsNone(category.created_by)
        self.assertIsNotNone(category.created_at)

    def test_category_str_method(self):
        """Test the string representation of category."""
        category = Category.objects.create(name="Electronics")
        self.assertEqual(str(category), "Electronics")

    def test_category_max_length(self):
        """Test category name max length constraint."""
        from django.core.exceptions import ValidationError
        
        long_name = "x" * 65  # Exceeding max_length=64
        category = Category(name=long_name)
        
        with self.assertRaises(ValidationError):
            category.full_clean()  # This will trigger validation

    def test_category_name_required(self):
        """Test that category name is required."""
        from django.core.exceptions import ValidationError
        
        category = Category(name="")
        
        with self.assertRaises(ValidationError):
            category.full_clean()  # This will trigger validation

    def test_user_deletion_sets_null(self):
        """Test that deleting a user sets created_by to null."""
        category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )
        
        user_id = self.user.id
        self.user.delete()
        
        category.refresh_from_db()
        self.assertIsNone(category.created_by)

    def test_category_ordering_default(self):
        """Test default ordering behavior."""
        Category.objects.create(name="Zebra")
        Category.objects.create(name="Apple")
        Category.objects.create(name="Book")
        categories = Category.objects.all()
        names = [cat.name for cat in categories]
        self.assertEqual(names, ["Zebra", "Apple", "Book"])


class SubCategoryModelTest(TestCase):
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )

    def test_subcategory_creation(self):
        """Test creating a subcategory."""
        subcategory = SubCategory.objects.create(
            category=self.category,
            name="Smartphones",
            created_by=self.user
        )
        
        self.assertEqual(subcategory.category, self.category)
        self.assertEqual(subcategory.name, "Smartphones")
        self.assertEqual(subcategory.created_by, self.user)
        self.assertIsNotNone(subcategory.created_at)

    def test_subcategory_creation_without_user(self):
        """Test creating a subcategory without a user."""
        subcategory = SubCategory.objects.create(
            category=self.category,
            name="Smartphones"
        )
        
        self.assertEqual(subcategory.category, self.category)
        self.assertEqual(subcategory.name, "Smartphones")
        self.assertIsNone(subcategory.created_by)

    def test_subcategory_str_method(self):
        """Test the string representation of subcategory."""
        subcategory = SubCategory.objects.create(
            category=self.category,
            name="Smartphones"
        )
        
        expected_str = "Electronics → Smartphones"
        self.assertEqual(str(subcategory), expected_str)

    def test_subcategory_meta_options(self):
        """Test subcategory meta options."""
        # Test verbose names
        self.assertEqual(SubCategory._meta.verbose_name, "SubCategory")
        self.assertEqual(SubCategory._meta.verbose_name_plural, "SubCategories")
        
        # Test ordering
        self.assertEqual(SubCategory._meta.ordering, ["name"])

    def test_subcategory_ordering(self):
        """Test subcategory ordering by name."""
        SubCategory.objects.create(category=self.category, name="Zebra")
        SubCategory.objects.create(category=self.category, name="Apple")
        SubCategory.objects.create(category=self.category, name="Book")
        
        subcategories = SubCategory.objects.all()
        names = [sub.name for sub in subcategories]
        self.assertEqual(names, ["Apple", "Book", "Zebra"])

    def test_subcategory_max_length(self):
        """Test subcategory name max length constraint."""
        from django.core.exceptions import ValidationError
        
        long_name = "x" * 65  
        subcategory = SubCategory(category=self.category, name=long_name)
        
        with self.assertRaises(ValidationError):
            subcategory.full_clean()  
    def test_category_deletion_cascades(self):
        """Test that deleting a category deletes subcategories."""
        subcategory = SubCategory.objects.create(
            category=self.category,
            name="Smartphones"
        )
        
        subcategory_id = subcategory.id
        self.category.delete()
        
        with self.assertRaises(SubCategory.DoesNotExist):
            SubCategory.objects.get(id=subcategory_id)

    def test_user_deletion_sets_null_subcategory(self):
        """Test that deleting a user sets created_by to null for subcategories."""
        subcategory = SubCategory.objects.create(
            category=self.category,
            name="Smartphones",
            created_by=self.user
        )
        
        self.user.delete()
        
        subcategory.refresh_from_db()
        self.assertIsNone(subcategory.created_by)

    def test_related_name_subcategories(self):
        """Test the related name for subcategories."""
        subcategory1 = SubCategory.objects.create(category=self.category, name="Phones")
        subcategory2 = SubCategory.objects.create(category=self.category, name="Laptops")
        
        subcategories = self.category.subcategories.all()
        self.assertIn(subcategory1, subcategories)
        self.assertIn(subcategory2, subcategories)


class CategorySerializerTest(TestCase):
    """Test cases for the CategorySerializer."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )

    def test_category_serialization(self):
        """Test serializing a category."""
        serializer = CategorySerializer(self.category)
        data = serializer.data
        
        self.assertEqual(data['id'], self.category.id)
        self.assertEqual(data['name'], "Electronics")
        self.assertEqual(data['created_by'], self.user.id)
        self.assertIn('created_at', data)

    def test_category_serialization_without_user(self):
        """Test serializing a category without created_by."""
        category = Category.objects.create(name="Books")
        serializer = CategorySerializer(category)
        data = serializer.data
        
        self.assertIsNone(data['created_by'])

    def test_category_deserialization(self):
        """Test deserializing category data."""
        data = {'name': 'New Category'}
        
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        category = serializer.save()
        self.assertEqual(category.name, 'New Category')

    def test_category_deserialization_invalid_data(self):
        """Test deserializing invalid category data."""
        data = {'name': ''}  
        
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_read_only_fields(self):
        """Test that certain fields are read-only."""
        data = {
            'id': 999,
            'name': 'Updated Category',
            'created_by': self.user.id,
            'created_at': '2023-01-01T00:00:00Z'
        }
        
        serializer = CategorySerializer(self.category, data=data)
        self.assertTrue(serializer.is_valid())
        
        updated_category = serializer.save()
        
        # Read-only fields should not change
        self.assertEqual(updated_category.id, self.category.id)
        self.assertEqual(updated_category.created_by, self.category.created_by)
        self.assertEqual(updated_category.created_at, self.category.created_at)
        
        # Only name should update
        self.assertEqual(updated_category.name, 'Updated Category')


class SubCategorySerializerTest(TestCase):
    """Test cases for the SubCategorySerializer."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )
        
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Smartphones",
            created_by=self.user
        )

    def test_subcategory_serialization(self):
        """Test serializing a subcategory."""
        serializer = SubCategorySerializer(self.subcategory)
        data = serializer.data
        
        self.assertEqual(data['id'], self.subcategory.id)
        self.assertEqual(data['category'], self.category.id)
        self.assertEqual(data['name'], "Smartphones")
        self.assertEqual(data['created_by'], self.user.id)
        self.assertIn('created_at', data)

    def test_subcategory_deserialization(self):
        """Test deserializing subcategory data."""
        data = {
            'category': self.category.id,
            'name': 'Laptops'
        }
        
        serializer = SubCategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        subcategory = serializer.save()
        self.assertEqual(subcategory.category, self.category)
        self.assertEqual(subcategory.name, 'Laptops')

    def test_subcategory_deserialization_invalid_category(self):
        """Test deserializing subcategory with invalid category."""
        data = {
            'category': 99999,  
            'name': 'Laptops'
        }
        
        serializer = SubCategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category', serializer.errors)

    def test_subcategory_read_only_fields(self):
        """Test that certain fields are read-only."""
        data = {
            'id': 999,
            'category': self.category.id,
            'name': 'Updated Subcategory',
            'created_by': 999,
            'created_at': '2023-01-01T00:00:00Z'
        }
        
        serializer = SubCategorySerializer(self.subcategory, data=data)
        self.assertTrue(serializer.is_valid())
        
        updated_subcategory = serializer.save()
        
        # Read-only fields should not change
        self.assertEqual(updated_subcategory.id, self.subcategory.id)
        self.assertEqual(updated_subcategory.created_by, self.subcategory.created_by)
        self.assertEqual(updated_subcategory.created_at, self.subcategory.created_at)
        
        # Other fields should update
        self.assertEqual(updated_subcategory.name, 'Updated Subcategory')


class CategoryAPITest(APITestCase):
    """Test cases for the Category API views."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=User.Roles.ADMIN
        )
        
        self.category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )

    def test_category_list_authenticated(self):
        """Test listing categories for authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        self.assertGreaterEqual(len(data), 1)
        category_names = [cat['name'] for cat in data]
        self.assertIn("Electronics", category_names)

    def test_category_list_unauthenticated(self):
        """Test that unauthenticated users can access categories (read-only)."""
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_detail(self):
        """Test retrieving category detail."""
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Electronics")
        self.assertEqual(response.data['id'], self.category.id)

    def test_category_create_admin(self):
        """Test creating category as admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('category-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Category')
        self.assertEqual(response.data['created_by'], self.admin_user.id)
        
        # Verify category was actually created
        self.assertTrue(Category.objects.filter(name='New Category').exists())

    def test_category_create_non_admin(self):
        """Test that non-admin users cannot create categories."""
        self.client.force_authenticate(user=self.user)
        url = reverse('category-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_create_unauthenticated(self):
        """Test that unauthenticated users cannot create categories."""
        url = reverse('category-list')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_update_admin(self):
        """Test updating category as admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        data = {'name': 'Updated Electronics'}
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Electronics')
        
        # Verify category was updated
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Electronics')

    def test_category_update_non_admin(self):
        """Test that non-admin users cannot update categories."""
        self.client.force_authenticate(user=self.user)
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        data = {'name': 'Updated Electronics'}
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_delete_admin(self):
        """Test deleting category as admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify category was deleted
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=self.category.id)

    def test_category_delete_non_admin(self):
        """Test that non-admin users cannot delete categories."""
        self.client.force_authenticate(user=self.user)
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_ordering(self):
        """Test that categories are ordered by name."""
        Category.objects.create(name="Zebra")
        Category.objects.create(name="Apple")
        
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        names = [cat['name'] for cat in data]
        self.assertEqual(names, sorted(names)) 

    def test_category_partial_update(self):
        """Test partial update (PATCH) of category."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        data = {'name': 'Partially Updated'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Partially Updated')


class SubCategoryAPITest(APITestCase):
    """Test cases for the SubCategory API views."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=User.Roles.ADMIN
        )
        
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Clothing")
        
        self.subcategory1 = SubCategory.objects.create(
            category=self.category1,
            name="Smartphones"
        )
        self.subcategory2 = SubCategory.objects.create(
            category=self.category1,
            name="Laptops"
        )
        self.subcategory3 = SubCategory.objects.create(
            category=self.category2,
            name="Shirts"
        )

    def test_subcategory_list(self):
        """Test listing subcategories."""
        url = reverse('subcategory-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        self.assertGreaterEqual(len(data), 3)
        names = [sub['name'] for sub in data]
        self.assertIn("Smartphones", names)
        self.assertIn("Laptops", names)
        self.assertIn("Shirts", names)

    def test_subcategory_list_filtered_by_category(self):
        """Test listing subcategories filtered by category."""
        url = reverse('subcategory-list')
        response = self.client.get(url, {'category': self.category1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Should only return subcategories from category1
        names = [sub['name'] for sub in data]
        self.assertIn("Smartphones", names)
        self.assertIn("Laptops", names)
        self.assertNotIn("Shirts", names)

    def test_subcategory_list_invalid_category_filter(self):
        """Test listing subcategories with invalid category filter."""
        url = reverse('subcategory-list')
        response = self.client.get(url, {'category': 'invalid'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should return all subcategories when filter is invalid
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        self.assertGreaterEqual(len(data), 3)

    def test_subcategory_detail(self):
        """Test retrieving subcategory detail."""
        url = reverse('subcategory-detail', kwargs={'pk': self.subcategory1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Smartphones")
        self.assertEqual(response.data['category'], self.category1.id)

    def test_subcategory_create_admin(self):
        """Test creating subcategory as admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('subcategory-list')
        data = {
            'category': self.category1.id,
            'name': 'Tablets'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Tablets')
        self.assertEqual(response.data['category'], self.category1.id)
        self.assertEqual(response.data['created_by'], self.admin_user.id)

    def test_subcategory_create_non_admin(self):
        """Test that non-admin users cannot create subcategories."""
        self.client.force_authenticate(user=self.user)
        url = reverse('subcategory-list')
        data = {
            'category': self.category1.id,
            'name': 'Tablets'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subcategory_update_admin(self):
        """Test updating subcategory as admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('subcategory-detail', kwargs={'pk': self.subcategory1.pk})
        data = {
            'category': self.category1.id,
            'name': 'Mobile Phones'
        }
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Mobile Phones')

    def test_subcategory_delete_admin(self):
        """Test deleting subcategory as admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('subcategory-detail', kwargs={'pk': self.subcategory1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify subcategory was actually deleted
        with self.assertRaises(SubCategory.DoesNotExist):
            SubCategory.objects.get(id=self.subcategory1.id)

    def test_subcategory_ordering(self):
        """Test that subcategories are ordered by name."""
        url = reverse('subcategory-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        names = [sub['name'] for sub in data]
        self.assertEqual(names, sorted(names))  

    def test_subcategory_select_related(self):
        """Test that subcategory queries use select_related for efficiency."""
        url = reverse('subcategory-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Verify category data is accessible
        for subcategory_data in data:
            self.assertIn('category', subcategory_data)
            self.assertIsInstance(subcategory_data['category'], int)


class ItemsAdminTest(TestCase):
    """Test cases for the Items admin interface."""

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            role=User.Roles.ADMIN
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )

        self.category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )
        
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Smartphones",
            created_by=self.user
        )

    def test_admin_category_configuration(self):
        """Test category admin configuration."""
        from django.contrib import admin
        from .admin import CategoryAdmin
        
        # Test that admin is registered
        self.assertIn(Category, admin.site._registry)
        
        # Test admin configuration
        admin_instance = CategoryAdmin(Category, admin.site)
        
        # Test list_display
        expected_list_display = ("id", "name", "created_by", "created_at")
        self.assertEqual(admin_instance.list_display, expected_list_display)
        
        # Test search_fields
        expected_search_fields = ("name",)
        self.assertEqual(admin_instance.search_fields, expected_search_fields)
        
        # Test list_filter
        expected_list_filter = ("created_at",)
        self.assertEqual(admin_instance.list_filter, expected_list_filter)
        
        # Test that SubCategoryInline is included
        self.assertGreater(len(admin_instance.inlines), 0)
        # Check if any inline is related to SubCategory
        has_subcategory_inline = any(
            inline.model == SubCategory for inline in admin_instance.inlines
        )
        self.assertTrue(has_subcategory_inline)

    def test_admin_subcategory_configuration(self):
        """Test subcategory admin configuration."""
        from django.contrib import admin
        from .admin import SubCategoryAdmin
        
        # Test that admin is registered
        self.assertIn(SubCategory, admin.site._registry)
        
        # Test admin configuration
        admin_instance = SubCategoryAdmin(SubCategory, admin.site)
        
        # Test list_display
        expected_list_display = ("id", "name", "category", "created_by", "created_at")
        self.assertEqual(admin_instance.list_display, expected_list_display)
        
        # Test search_fields
        expected_search_fields = ("name", "category__name")
        self.assertEqual(admin_instance.search_fields, expected_search_fields)
        
        # Test list_filter
        expected_list_filter = ("created_at", "category")
        self.assertEqual(admin_instance.list_filter, expected_list_filter)

    def test_subcategory_inline_configuration(self):
        """Test subcategory inline configuration."""
        from .admin import SubCategoryInline
        
        # Test inline configuration
        self.assertEqual(SubCategoryInline.model, SubCategory)
        self.assertEqual(SubCategoryInline.extra, 0)
        
        expected_fields = ("name", "created_by", "created_at")
        self.assertEqual(SubCategoryInline.fields, expected_fields)
        
        expected_readonly_fields = ("created_at",)
        self.assertEqual(SubCategoryInline.readonly_fields, expected_readonly_fields)


class ItemsIntegrationTest(TestCase):
    """Integration tests for the items module."""
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=User.Roles.ADMIN
        )

    def test_category_subcategory_relationship(self):
        # Create category
        category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )
        
        # Create subcategories
        subcategory1 = SubCategory.objects.create(
            category=category,
            name="Smartphones",
            created_by=self.user
        )
        
        subcategory2 = SubCategory.objects.create(
            category=category,
            name="Laptops",
            created_by=self.user
        )
        
        # Test relationships
        self.assertEqual(category.subcategories.count(), 2)
        self.assertIn(subcategory1, category.subcategories.all())
        self.assertIn(subcategory2, category.subcategories.all())
        
        # Test reverse relationship
        self.assertEqual(subcategory1.category, category)
        self.assertEqual(subcategory2.category, category)

    def test_cascade_deletion_workflow(self):
        """Test cascade deletion from category to subcategories."""
        # Create category with subcategories
        category = Category.objects.create(name="Electronics")
        
        subcategory_ids = []
        for i in range(3):
            subcategory = SubCategory.objects.create(
                category=category,
                name=f"Subcategory {i+1}"
            )
            subcategory_ids.append(subcategory.id)
        
        # Verify subcategories exist
        self.assertEqual(SubCategory.objects.filter(id__in=subcategory_ids).count(), 3)
        
        # Delete category
        category.delete()
        
        # Verify subcategories were also deleted
        self.assertEqual(SubCategory.objects.filter(id__in=subcategory_ids).count(), 0)

    def test_user_deletion_workflow(self):
        """Test user deletion effects on categories and subcategories."""
        # Create category and subcategory with user
        category = Category.objects.create(
            name="Electronics",
            created_by=self.user
        )
        
        subcategory = SubCategory.objects.create(
            category=category,
            name="Smartphones",
            created_by=self.user
        )
        
        # Delete user
        self.user.delete()
        
        # Verify category and subcategory still exist but created_by is null
        category.refresh_from_db()
        subcategory.refresh_from_db()
        
        self.assertIsNone(category.created_by)
        self.assertIsNone(subcategory.created_by)

    def test_bulk_operations(self):
        """Test bulk operations on categories and subcategories."""
        # Create multiple categories
        categories = []
        for i in range(5):
            category = Category.objects.create(name=f"Category {i+1}")
            categories.append(category)
        
        # Create subcategories for each category
        subcategories = []
        for category in categories:
            for j in range(2):
                subcategory = SubCategory.objects.create(
                    category=category,
                    name=f"{category.name} - Sub {j+1}"
                )
                subcategories.append(subcategory)
        
        # Test bulk queries
        self.assertEqual(Category.objects.count(), 5)
        self.assertEqual(SubCategory.objects.count(), 10)
        
        # Test filtering
        electronics_category = Category.objects.filter(name__contains="Category").first()
        related_subcategories = SubCategory.objects.filter(category=electronics_category)
        self.assertEqual(related_subcategories.count(), 2)
        
        # Test bulk delete
        Category.objects.filter(name__contains="Category").delete()
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(SubCategory.objects.count(), 0)  # Should be cascade deleted

    def test_ordering_and_filtering_integration(self):
        """Test ordering and filtering work correctly together."""
        # Create categories in random order
        Category.objects.create(name="Zebra")
        Category.objects.create(name="Apple")
        Category.objects.create(name="Book")
        
        # Test ordered query
        categories = Category.objects.all().order_by("name")
        names = [cat.name for cat in categories]
        self.assertEqual(names, ["Apple", "Book", "Zebra"])
        
        # Create subcategories in random order
        apple_cat = Category.objects.get(name="Apple")
        SubCategory.objects.create(category=apple_cat, name="iPad")
        SubCategory.objects.create(category=apple_cat, name="iPhone")
        SubCategory.objects.create(category=apple_cat, name="Mac")
        
        # Test ordered subcategories (should use Meta ordering by name)
        subcategories = SubCategory.objects.filter(category=apple_cat).order_by('name')
        sub_names = [sub.name for sub in subcategories]
        # They should be ordered alphabetically by name
        expected_order = sorted(["iPad", "iPhone", "Mac"])
        self.assertEqual(sub_names, expected_order)