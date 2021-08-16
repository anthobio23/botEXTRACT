simport spandas

ds = pandas.read_excel("scraping_data.xlsx",
        sheet_name="Sostenes", header=None,
        names=["produc", "Cant/char", "CodUniversal", 
            "color", "colo_comercial", "talla", "img",
            "sku", "cantidad", "Precio", "Moneda", "Condicion",
            "Desc", "link", "tipPublicacion", "formaenvio",
            "costoenvio", "retiropersona", "garantia", "tiempogarantia",
            "unidad_garantia", "Marca", "Modelo", "cant_pack", "genero",
            "composicion", "material", "tipoBombacha", 
            "apta_embarazadas"])
print(ds.head(10))




