use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use serde_json;
use stac::{Catalog, Collection, Links};
use std::{fs, path::Path};

#[pyfunction]
fn print_stac_catalog_collections(path: &str) -> PyResult<()> {
    let catalog: stac::Catalog = stac::read(path).map_err(|e| {
        PyErr::new::<PyRuntimeError, _>(format!("Error al leer el catálogo: {}", e))
    })?;
    for link in catalog.iter_child_links() {
        if link.rel == "child" && link.href.ends_with("collection.json") {
            println!("{}", &link.href);
        }
    }
    Ok(())
}

#[pyfunction]
fn print_stac_catalog(path: &str) -> PyResult<()> {
    let catalog: stac::Catalog = stac::read(path).map_err(|e| {
        PyErr::new::<PyRuntimeError, _>(format!("Error al leer el catálogo: {}", e))
    })?;
    let catalog_json = serde_json::to_string(&catalog).map_err(|e| {
        PyErr::new::<PyRuntimeError, _>(format!("Error al serializar a JSON: {}", e))
    })?;
    println!("{}", catalog_json);
    Ok(())
}

#[pyfunction]
fn save_stac_catalog(path: &str) -> PyResult<()> {
    let catalog: stac::Catalog = stac::read(path).map_err(|e| {
        PyErr::new::<PyRuntimeError, _>(format!("Error al leer el catálogo: {}", e))
    })?;
    let catalog_json = serde_json::to_string(&catalog).map_err(|e| {
        PyErr::new::<PyRuntimeError, _>(format!("Error al serializar a JSON: {}", e))
    })?;
    let output_dir = Path::new("output");
    if !output_dir.exists() {
        fs::create_dir(output_dir).map_err(|e| {
            PyErr::new::<PyRuntimeError, _>(format!("Error al crear la carpeta 'output': {}", e))
        })?;
    }

    let output_path = output_dir.join("catalog.json");
    fs::write(&output_path, catalog_json).map_err(|e| {
        PyErr::new::<PyRuntimeError, _>(format!("Error al guardar el archivo JSON: {}", e))
    })?;
    Ok(())
}

#[pymodule]
fn hyperstac(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(print_stac_catalog, m)?)?;
    m.add_function(wrap_pyfunction!(save_stac_catalog, m)?)?;
    m.add_function(wrap_pyfunction!(print_stac_catalog_collections, m)?)?;
    Ok(())
}
