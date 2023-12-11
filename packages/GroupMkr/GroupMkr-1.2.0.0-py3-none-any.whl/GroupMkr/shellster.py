from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# import User model
from django.contrib.auth.models import User


def add_group(group_name, permitt):
    try:
        group_name = group_name.strip()  # Remove leading/trailing spaces

        # Check if the group already exists
        existing_group = Group.objects.filter(name=group_name).first()
        if existing_group:
            return True, f"A group with the name '{group_name}' already exists"

        # Create or get the group
        new_group, created = Group.objects.get_or_create(name=group_name)

        # Get content type for the User model
        ct = ContentType.objects.get_for_model(User)

        # Create permission codename
        permit_codename = permitt.replace(" ", "_")

        # Create or get the permission
        permission, created = Permission.objects.get_or_create(
            codename=permit_codename,
            content_type=ct,
            defaults={'name': permitt}
        )

        # Check if the permission is already assigned to the group
        if permission not in new_group.permissions.all():
            # Add permission to the group
            new_group.permissions.add(permission)

        return True, "Group and permission added successfully"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
