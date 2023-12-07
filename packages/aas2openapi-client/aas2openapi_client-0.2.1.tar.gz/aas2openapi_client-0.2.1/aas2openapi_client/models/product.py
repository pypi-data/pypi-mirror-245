from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bom import BOM
    from ..models.construction_data import ConstructionData
    from ..models.process_reference import ProcessReference
    from ..models.product_information import ProductInformation


T = TypeVar("T", bound="Product")


@attr.s(auto_attribs=True)
class Product:
    """AAS to describe a product.

    Args:
        id_ (str): The id of the product.
        description (Optional[str]): The description of the product.
        id_short (Optional[str]): The short id of the product.
        semantic_id (Optional[str]): The semantic id of the product.
        construction_data (Optional[ConstructionData]): The construction data of the product.
        bom (Optional[BOM]): The bill of materials of the product.
        process_reference (Optional[ProcessReference]): The process reference of the product.

        Attributes:
            id_short (str):
            id (str):
            description (Union[Unset, str]):
            product_information (Union[Unset, ProductInformation]): Submodel to describe general information of the product.

                Args:
                    id_ (str): The id of the product general information.
                    description (Optional[str]): The description of the product general information.
                    id_short (Optional[str]): The short id of the product general information.
                    semantic_id (Optional[str]): The semantic id of the product general information.
                    product_type (str): The type of the product.
                    manufacturer (str): The manufacturer of the product.
            construction_data (Union[Unset, ConstructionData]): Submodel to describe the construction data of a product.

                Args:
                    id_ (str): The id of the construction data.
                    description (Optional[str]): The description of the construction data.
                    id_short (Optional[str]): The short id of the construction data.
                    semantic_id (Optional[str]): The semantic id of the construction data.
                    cad_file (Optional[str]): IRI to a CAD file of the product.
            bom (Union[Unset, BOM]): Submodel to describe the bill of materials of a product.

                Args:
                    id_ (str): The id of the bill of materials.
                    description (Optional[str]): The description of the bill of materials.
                    id_short (Optional[str]): The short id of the bill of materials.
                    semantic_id (Optional[str]): The semantic id of the bill of materials.
                    sub_product_count (Optional[int]): The total number of subproducts (depht 1)
                    sub_products (Optional[List[SubmodelElementCollection]]): The list of subproducts contained in the product
                (depht 1)
            process_reference (Union[Unset, ProcessReference]): Submodel to reference process to create a product.

                Args:
                    id_ (str): The id of the process reference.
                    description (Optional[str]): The description of the process reference.
                    id_short (Optional[str]): The short id of the process reference.
                    semantic_id (Optional[str]): The semantic id of the process reference.
                    process_id (str): reference to the process to create the product
                    alternative_process_ids (Optional[List[str]]): alternative processes to create the product
    """

    id_short: str
    id: str
    description: Union[Unset, str] = UNSET
    product_information: Union[Unset, "ProductInformation"] = UNSET
    construction_data: Union[Unset, "ConstructionData"] = UNSET
    bom: Union[Unset, "BOM"] = UNSET
    process_reference: Union[Unset, "ProcessReference"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id_short = self.id_short
        id = self.id
        description = self.description
        product_information: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.product_information, Unset):
            product_information = self.product_information.to_dict()

        construction_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.construction_data, Unset):
            construction_data = self.construction_data.to_dict()

        bom: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bom, Unset):
            bom = self.bom.to_dict()

        process_reference: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.process_reference, Unset):
            process_reference = self.process_reference.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id_short": id_short,
                "id_": id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if product_information is not UNSET:
            field_dict["product_information"] = product_information
        if construction_data is not UNSET:
            field_dict["construction_data"] = construction_data
        if bom is not UNSET:
            field_dict["bom"] = bom
        if process_reference is not UNSET:
            field_dict["process_reference"] = process_reference

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.bom import BOM
        from ..models.construction_data import ConstructionData
        from ..models.process_reference import ProcessReference
        from ..models.product_information import ProductInformation

        d = src_dict.copy()
        id_short = d.pop("id_short")

        id = d.pop("id_")

        description = d.pop("description", UNSET)

        _product_information = d.pop("product_information", UNSET)
        product_information: Union[Unset, ProductInformation]
        if isinstance(_product_information, Unset):
            product_information = UNSET
        else:
            product_information = ProductInformation.from_dict(_product_information)

        _construction_data = d.pop("construction_data", UNSET)
        construction_data: Union[Unset, ConstructionData]
        if isinstance(_construction_data, Unset):
            construction_data = UNSET
        else:
            construction_data = ConstructionData.from_dict(_construction_data)

        _bom = d.pop("bom", UNSET)
        bom: Union[Unset, BOM]
        if isinstance(_bom, Unset):
            bom = UNSET
        else:
            bom = BOM.from_dict(_bom)

        _process_reference = d.pop("process_reference", UNSET)
        process_reference: Union[Unset, ProcessReference]
        if isinstance(_process_reference, Unset):
            process_reference = UNSET
        else:
            process_reference = ProcessReference.from_dict(_process_reference)

        product = cls(
            id_short=id_short,
            id=id,
            description=description,
            product_information=product_information,
            construction_data=construction_data,
            bom=bom,
            process_reference=process_reference,
        )

        product.additional_properties = d
        return product

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
