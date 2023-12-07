from app.core.examples.examples_schema import Example


def test_example_schema():
    """Test example schema."""
    example = Example(
        id=1,
        name="example",
        description="example description"
    )
    assert example.id == 1
    assert example.name == "example"
    assert example.description == "example description"
