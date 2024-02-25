import django
import pytest
django.setup()


@pytest.mark.django_db
def test_event_serializer():
    from events.serializers import EventSerializer
    event_data = {
        'name': 'Test Event',
        'start_date': '2024-02-26T12:00:00Z',
        'end_date': '2024-02-27T12:00:00Z',
        'description': 'This is a test event',
        'owner': 'testuser',
        'attendees': []
    }
    serializer = EventSerializer(data=event_data)
    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_event_serializer_invalid_end_date():
    from events.serializers import EventSerializer
    event_data = {
        'name': 'Test Event',
        'start_date': '2024-02-26T12:00:00Z',
        'end_date': '2024-02-25T12:00:00Z',
        'description': 'This is a test event',
        'owner': 'testuser',
        'attendees': []
    }
    serializer = EventSerializer(data=event_data)
    assert not serializer.is_valid(), serializer.errors
    assert 'End date must be after start date.' in serializer.errors['non_field_errors']


@pytest.mark.django_db
def test_event_serializer_missing_required_field():
    from events.serializers import EventSerializer
    event_data = {
        'start_date': '2024-02-26T12:00:00Z',
        'end_date': '2024-02-27T12:00:00Z',
        'description': 'This is a test event',
        'owner': 'testuser',
        'attendees': []
    }

    serializer = EventSerializer(data=event_data)
    assert not serializer.is_valid()
    assert 'name' in serializer.errors


@pytest.mark.django_db
def test_register_serializer():
    from events.serializers import RegisterSerializer
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'strong_password',
        'password2': 'strong_password'
    }
    serializer = RegisterSerializer(data=user_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_register_serializer_password_mismatch():
    from events.serializers import RegisterSerializer
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'strong_password',
        'password2': 'different_password'  # Password mismatch
    }
    serializer = RegisterSerializer(data=user_data)
    assert not serializer.is_valid()
    assert 'Password fields didn\'t match.' in serializer.errors['password']
