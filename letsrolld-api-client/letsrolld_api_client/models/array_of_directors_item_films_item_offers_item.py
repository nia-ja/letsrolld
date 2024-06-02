from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ArrayOfDirectorsItemFilmsItemOffersItem")


@_attrs_define
class ArrayOfDirectorsItemFilmsItemOffersItem:
    """
    Attributes:
        name (str):
        url (Union[None, str]):
    """

    name: str
    url: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        url: Union[None, str]
        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        url = _parse_url(d.pop("url"))

        array_of_directors_item_films_item_offers_item = cls(
            name=name,
            url=url,
        )

        array_of_directors_item_films_item_offers_item.additional_properties = d
        return array_of_directors_item_films_item_offers_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
