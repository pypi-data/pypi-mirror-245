from geokoord.enums import Publisher, PublisherAcronym


def test_equal_keys():
    """Test if the keys of PublisherAcronym and Publisher are equal."""
    assert PublisherAcronym._member_names_ == Publisher._member_names_
