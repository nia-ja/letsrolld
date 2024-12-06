from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.array_of_reports_item_sections_item import ArrayOfReportsItemSectionsItem


T = TypeVar("T", bound="ArrayOfReportsItem")


@_attrs_define
class ArrayOfReportsItem:
    """
    Attributes:
        id (int):
        name (str):
        sections (Union[Unset, List['ArrayOfReportsItemSectionsItem']]):
    """

    id: int
    name: str
    sections: Union[Unset, List["ArrayOfReportsItemSectionsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        sections: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.sections, Unset):
            sections = []
            for sections_item_data in self.sections:
                sections_item = sections_item_data.to_dict()
                sections.append(sections_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if sections is not UNSET:
            field_dict["sections"] = sections

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.array_of_reports_item_sections_item import ArrayOfReportsItemSectionsItem

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        sections = []
        _sections = d.pop("sections", UNSET)
        for sections_item_data in _sections or []:
            sections_item = ArrayOfReportsItemSectionsItem.from_dict(sections_item_data)

            sections.append(sections_item)

        array_of_reports_item = cls(
            id=id,
            name=name,
            sections=sections,
        )

        array_of_reports_item.additional_properties = d
        return array_of_reports_item

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
