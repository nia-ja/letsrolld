from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.report_sections_item_films_item import ReportSectionsItemFilmsItem


T = TypeVar("T", bound="ReportSectionsItem")


@_attrs_define
class ReportSectionsItem:
    """
    Attributes:
        name (str):
        films (List['ReportSectionsItemFilmsItem']):
    """

    name: str
    films: List["ReportSectionsItemFilmsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        films = []
        for films_item_data in self.films:
            films_item = films_item_data.to_dict()
            films.append(films_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "films": films,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.report_sections_item_films_item import ReportSectionsItemFilmsItem

        d = src_dict.copy()
        name = d.pop("name")

        films = []
        _films = d.pop("films")
        for films_item_data in _films:
            films_item = ReportSectionsItemFilmsItem.from_dict(films_item_data)

            films.append(films_item)

        report_sections_item = cls(
            name=name,
            films=films,
        )

        report_sections_item.additional_properties = d
        return report_sections_item

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
