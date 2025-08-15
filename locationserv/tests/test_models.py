from src.models import Location, GeoPoint, Address, AddressDistrict, CountryRegion
from bson import ObjectId

def test_location_model_fields():
    """Test Location model field assignment."""
    address = Address(
        countryRegion=CountryRegion(name="USA"),
        addressLine="123 Main St",
        adminDistricts=[AddressDistrict(name="District 1", shortName="D1")],
        formattedAddress="123 Main St, City, State, 12345",
        locality="City",
        postalCode="12345",
        streetName="Main St",
        streetNumber="123"
    )
    loc = Location(
        id=str(ObjectId()),  # Pass as string, not ObjectId
        name="Test",
        account_id="1",
        active=True,
        created_by="user1",
        geo_point=GeoPoint(type="Point", coordinates=[0.0, 0.0]),
        address=address
    )
    assert str(loc.id)  # id is ObjectId
    assert loc.name == "Test"
    assert loc.account_id == "1"
    assert loc.active is True
    assert loc.created_by == "user1"
    assert loc.geo_point.type == "Point"
    assert loc.geo_point.coordinates == [0.0, 0.0]
    assert isinstance(loc.address, Address)
    assert loc.address.countryRegion.name == "USA"
    assert loc.address.addressLine == "123 Main St"
    assert loc.address.adminDistricts[0].name == "District 1"
    assert loc.address.formattedAddress == "123 Main St, City, State, 12345"
    assert loc.address.locality == "City"
    assert loc.address.postalCode == "12345"
    assert loc.address.streetName == "Main St"
    assert loc.address.streetNumber == "123"