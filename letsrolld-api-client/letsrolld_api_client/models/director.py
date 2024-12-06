from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.director_films_item import DirectorFilmsItem
    from ..models.director_info import DirectorInfo


T = TypeVar("T", bound="Director")


@_attrs_define
class Director:
    """
    Attributes:
        info (DirectorInfo):
        films (Union[Unset, List['DirectorFilmsItem']]):
    """

    info: "DirectorInfo"
    films: Union[Unset, List["DirectorFilmsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        info = self.info.to_dict()

        films: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.films, Unset):
            films = []
            for films_item_data in self.films:
                films_item = films_item_data.to_dict()
                films.append(films_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "info": info,
            }
        )
        if films is not UNSET:
            field_dict["films"] = films

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.director_films_item import DirectorFilmsItem
        from ..models.director_info import DirectorInfo

        d = src_dict.copy()
        info = DirectorInfo.from_dict(d.pop("info"))

        films = []
        _films = d.pop("films", UNSET)
        for films_item_data in _films or []:
            films_item = DirectorFilmsItem.from_dict(films_item_data)

            films.append(films_item)

        director = cls(
            info=info,
            films=films,
        )

        director.additional_properties = d
        return director

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
