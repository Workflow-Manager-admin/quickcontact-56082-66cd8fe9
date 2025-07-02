from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields
import uuid
import json
import os

# Path to the JSON file for storing contacts
DATA_FILE = os.path.join(os.path.dirname(__file__), '../../contacts_data.json')

def load_contacts():
    """Load contacts from the JSON file."""
    print(f"[DEBUG] Loading contacts from {DATA_FILE}")
    if not os.path.exists(DATA_FILE):
        print("[DEBUG] Data file does not exist; returning empty list.")
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            contacts = json.load(f)
            print(f"[DEBUG] Loaded contacts: {contacts}")
            return contacts
        except json.JSONDecodeError:
            print("[ERROR] JSON decode error while loading contacts.")
            return []

def save_contacts(contacts):
    """Save contacts to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)

# Marshmallow Schemas

class ContactSchema(Schema):
    id = fields.String(dump_only=True, description="Contact unique identifier")
    name = fields.String(required=True, description="Full name of the contact")
    email = fields.Email(required=True, description="Email address of the contact")
    phone = fields.String(required=True, description="Phone number of the contact")

class ContactCreateSchema(Schema):
    name = fields.String(required=True, description="Full name of the contact")
    email = fields.Email(required=True, description="Email address of the contact")
    phone = fields.String(required=True, description="Phone number of the contact")

# Flask-Smorest Blueprint
blp = Blueprint(
    "Contacts", "contacts", url_prefix="/contacts",
    description="API endpoints for managing contacts"
)

# PUBLIC_INTERFACE
@blp.route("/")
class ContactsList(MethodView):
    """Handles listing and adding contacts."""
    # PUBLIC_INTERFACE
    @blp.response(200, ContactSchema(many=True), description="List of all contacts")
    def get(self):
        """Get the list of all contacts."""
        print("[DEBUG] GET request received at /contacts/")
        contacts = load_contacts()
        print(f"[DEBUG] Returning contacts list of size {len(contacts)}")
        return contacts

    # PUBLIC_INTERFACE
    @blp.arguments(ContactCreateSchema, location="json")
    @blp.response(201, ContactSchema, description="The newly created contact")
    def post(self, new_data):
        """Add a new contact."""
        print(f"[DEBUG] POST request received at /contacts/ with data: {new_data}")
        contacts = load_contacts()
        new_contact = {
            "id": str(uuid.uuid4()),
            "name": new_data["name"],
            "email": new_data["email"],
            "phone": new_data["phone"]
        }
        contacts.append(new_contact)
        try:
            save_contacts(contacts)
            print(f"[DEBUG] New contact created and saved: {new_contact}")
        except Exception as e:
            print(f"[ERROR] Exception while saving new contact: {e}")
        return new_contact

# PUBLIC_INTERFACE
@blp.route("/<contact_id>")
class ContactDetail(MethodView):
    """Handles deleting a contact."""
    # PUBLIC_INTERFACE
    @blp.response(204, description="Contact deleted successfully")
    def delete(self, contact_id):
        """Delete a contact by ID."""
        print(f"[DEBUG] DELETE request received at /contacts/{contact_id}")
        contacts = load_contacts()
        filtered = [c for c in contacts if c["id"] != contact_id]
        if len(filtered) == len(contacts):
            print(f"[DEBUG] Contact with id {contact_id} not found.")
            abort(404, message="Contact not found")
        save_contacts(filtered)
        print(f"[DEBUG] Deleted contact with id {contact_id}. Remaining: {len(filtered)}")
        return '', 204
