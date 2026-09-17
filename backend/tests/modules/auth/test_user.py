from src.modules.auth.database.model import User

def test_add_user(get_test_session):
    test_session = get_test_session

    user = User(email="andre@gmail.com")
    test_session.add(user)
    test_session.commit()
    
    saved_user = get_test_session.query(User).filter_by(email="andre@gmail.com").first()
     
    assert saved_user is not None
    assert saved_user.id is not None
    