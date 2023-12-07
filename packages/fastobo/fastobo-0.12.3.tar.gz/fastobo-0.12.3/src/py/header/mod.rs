pub mod clause;
pub mod frame;

use pyo3::prelude::*;

#[pymodule]
#[pyo3(name = "header")]
pub fn init(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<self::frame::HeaderFrame>()?;
    m.add_class::<self::clause::BaseHeaderClause>()?;
    m.add_class::<self::clause::FormatVersionClause>()?;
    m.add_class::<self::clause::DataVersionClause>()?;
    m.add_class::<self::clause::DateClause>()?;
    m.add_class::<self::clause::SavedByClause>()?;
    m.add_class::<self::clause::AutoGeneratedByClause>()?;
    m.add_class::<self::clause::ImportClause>()?;
    m.add_class::<self::clause::SubsetdefClause>()?;
    m.add_class::<self::clause::SynonymTypedefClause>()?;
    m.add_class::<self::clause::DefaultNamespaceClause>()?;
    m.add_class::<self::clause::IdspaceClause>()?;
    m.add_class::<self::clause::TreatXrefsAsEquivalentClause>()?;
    m.add_class::<self::clause::TreatXrefsAsGenusDifferentiaClause>()?;
    m.add_class::<self::clause::TreatXrefsAsReverseGenusDifferentiaClause>()?;
    m.add_class::<self::clause::TreatXrefsAsRelationshipClause>()?;
    m.add_class::<self::clause::TreatXrefsAsIsAClause>()?;
    m.add_class::<self::clause::TreatXrefsAsHasSubclassClause>()?;
    m.add_class::<self::clause::PropertyValueClause>()?;
    m.add_class::<self::clause::RemarkClause>()?;
    m.add_class::<self::clause::OntologyClause>()?;
    m.add_class::<self::clause::OwlAxiomsClause>()?;
    m.add_class::<self::clause::UnreservedClause>()?;
    m.add_class::<self::clause::NamespaceIdRuleClause>()?;

    register!(py, m, HeaderFrame, "collections.abc", MutableSequence);

    m.add("__name__", "fastobo.header")?;

    Ok(())
}
