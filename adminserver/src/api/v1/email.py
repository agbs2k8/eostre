import datetime
from quart import Blueprint, jsonify, g, request
from src.services.auth_manager import auth_manager
from src.services.smtp_handler import send_email, test_email
from src.models.models import User, Email, TokenEvent
import config as cfg
import logging

logger = logging.getLogger(__name__)
email_bp = Blueprint("email_v1", __name__, url_prefix="/email")


@email_bp.route("send_validate", methods=["POST"])
@auth_manager.jwt_required()
async def send_validation():
    async with g.db_session as session:
        user_id = g.user['sub']
        # TODO - replace 400 here with proper pydantic validation
        data = await request.get_json()
        new_email = data.get('email')
        if not new_email:
            return jsonify({"error": "No email address provided"}), 400
        
        # Ensure that the provided email address is not already in use
        if (existing := Email.find(new_email, session)):
            if existing.user_id == user_id:
                # If it belongs to the user in question, we can give them details
                return jsonify({"error": "The provided email is already validated."}), 406
            else:
                # If they are attempting to validate someone else's email, we may have problems
                logger.warning(f"User {user_id} attempted to validate an in-use email address")
                return jsonify({"error": "Unable to process the provided email address."}), 406
        
        # Look to see if we have an existing token for that user
        if (te := TokenEvent.find(new_email)):
            if te.created_for == user_id:  # If the email & user_id match, reset the expiration
                te.reset_expiration(user_id, hours_valid=2)
            else:
                # If the email and user_id don't match, we could have problems
                logger.warning(f"User {user_id} attempted to validate an pending email address")
                return jsonify({"error": "Unable to process the provided email address."}), 406
        else:
            # when no event exists (happy-path) we make one
            te = TokenEvent(type = "email", 
                            key = new_email,
                            created_by = user_id, 
                            created_for = user_id,
                            hours_valid = 2)
        await session.commit(te)
        token_url = await te.generate_url()
        logging.debug("token event updated and URL created.")
            
        # Build the email record to send
        logger.info(f"User {g.user['sub']} requesting new-email validation")
        user_record = await User.get(user_id, session)
        if user_record.display_name:
            name = user_record.display_name
        else:
            name = user_record.name
        if cfg.EMAIL_ENABLED:
            sent = await send_email(to_email=new_email,
                                    template="email_validation",
                                    name=name,
                                    verify_url=token_url,
                                    year=datetime.datetime.now().year
                                    )
        else: 
            return {"validation_url": token_url}
        if sent:
            return {"message": "ok"}, 200
        else:
            return {"error": "unable to send message"}, 500
    
