from edc_sites.single_site import SingleSite

fqdn = "clinicedc.org"
language_codes = ["en"]
sites: list[SingleSite] = [
    SingleSite(
        10,
        "mochudi",
        title="Mochudi",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        domain=f"mochudi.bw.{fqdn}",
    ),
    SingleSite(
        20,
        "molepolole",
        title="Molepolole",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        fqdn=fqdn,
    ),
    SingleSite(
        30,
        "lobatse",
        title="Lobatse",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        fqdn=fqdn,
    ),
    SingleSite(
        40,
        "gaborone",
        title="Gaborone",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        fqdn=fqdn,
    ),
    SingleSite(
        50,
        "karakobis",
        title="Karakobis",
        country="botswana",
        country_code="bw",
        language_codes=language_codes,
        fqdn=fqdn,
    ),
    SingleSite(
        60,
        "windhoek",
        title="Windhoek",
        country="namibia",
        country_code="na",
        language_codes=language_codes,
        fqdn=fqdn,
    ),
]


more_sites = [
    SingleSite(
        60,
        "windhoek",
        title="Windhoek",
        country="namibia",
        country_code="na",
        language_codes=language_codes,
        fqdn=fqdn,
    ),
]

all_sites = {"botswana": sites, "namibia": more_sites}
all_test_sites = {"botswana": sites, "namibia": more_sites}
