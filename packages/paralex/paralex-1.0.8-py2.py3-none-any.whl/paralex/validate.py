#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validates packages
"""
import frictionless as fl
from pathlib import Path
import json
from .meta import _get_default_package
from rich.console import Console
from rich.table import Table
from collections import defaultdict
import re
from enum import IntEnum
import pandas as pd

Status = IntEnum('Status', 'fails passes NA', start=0)

console = Console()
paralex = _get_default_package()


class ParalexValidator(object):
    pass_or_fail = (':X:', ':heavy_check_mark:', '')
    pass_or_flag = (':black_flag:', ':heavy_check_mark:', '')
    must_style = ("bold red", "green", "grey50")
    should_style = ("bold dark_orange3", "green", "grey50")

    def __init__(self, package_path):
        self.path = Path(package_path)

        with open(package_path, "r", encoding="utf-8") as f:
            self.p = fl.Package(json.load(f))
            self.p.basepath = str(self.path.parent)
        self.levels = {"musts": [self.is_valid,
                                 self.has_doc,
                                 self.has_forms,
                                 self.has_form_triplets,
                                 self.has_expected_foreign_keys,
                                 self.tags_are_defined,
                                 self.has_vocabulary_relations,
                                 self.has_conventional_cell_ids
                                 ],
                       "checks": [
                           self.has_coherent_analyses,
                           self.is_ipa_or_has_sounds_table,
                           self.has_atomic_forms,
                           self.has_cell_mapping,
                           self.has_feature_values_mapping,
                           self.has_space_separated_phon_form,
                           self.has_sounds_definition,
                           self.all_values_have_cells,
                           self.all_lexemes_have_forms,
                           self.all_cells_have_forms,
                           self.all_columns_have_metadata
                       ],
                       "shoulds": [
                           self.has_recommended_tables,
                           self.has_multiple_cell_mappings,
                           self.has_ids_first,
                           self.has_phon_form,
                           self.has_data_sheet,
                       ]
                       }
        self.styles = {"musts": (self.pass_or_fail, self.must_style),
                       "checks": (self.pass_or_flag, self.should_style),
                       "shoulds": (self.pass_or_fail, self.should_style)
                       }

        self.tables = {}
        self.standard_tables = (set(self.p.resource_names) & set(paralex.resource_names))

    def get_table(self, name):
        if name not in self.tables:
            self.tables[name] = pd.read_csv(Path(self.p.basepath) / self.p.get_resource(name).path)
        return self.tables[name]

    def is_valid(self):
        report = fl.validate(self.path)
        if report.valid:
            return (report.valid, "pass frictionless validation", "")
        return (report.valid,
                "did not pass frictionless validation.",
                "Run `frictionless validate <package>` for details.")

    def validate(self, level):
        icons, styles = self.styles[level]
        for task in self.levels[level]:
            status, report, solution = task()
            console.print("- " + icons[status] + ' ' + report, style=styles[status])
            if solution:
                console.print(" " + solution, style=styles[status])

    def has_expected_foreign_keys(self):

        error = "Could not find some foreign keys:\n\t- {}"
        suggestion = "Re-generate metadata using the paralex package"
        invalid_keys = []
        for table_name in self.standard_tables:
            table = self.p.get_resource(table_name)
            table_def = paralex.get_resource(table_name)

            table_refs = {
                (tuple(rel["fields"]),
                 rel["reference"]["resource"],
                 tuple(rel["reference"]["fields"]),
                 ) for rel in table.schema.foreign_keys}

            for rel in table_def.schema.foreign_keys:
                cols = tuple(rel["fields"])
                foreign_table = rel["reference"]["resource"]
                foreign_cols = tuple(rel["reference"]["fields"])
                ref = (cols, foreign_table, foreign_cols)

                if foreign_table in self.standard_tables and ref not in table_refs:
                    invalid = f"{table_name}.{'+'.join(cols)} => {foreign_table}.{'+'.join(foreign_cols)}"
                    invalid_keys.append(invalid)

        if invalid_keys:
            return (Status.fails, error.format("\n\t- ".join(invalid_keys)), suggestion)
        return (Status.passes, "Has all expected relations", "")

    def all_lexemes_have_forms(self):
        error = "Not all lexemes have forms: {}"
        if "lexemes" in self.standard_tables:
            lex = set(self.get_table("lexemes").lexeme_id.to_list())
            forms = set(self.get_table("forms").lexeme.to_list())
            unref_lex = lex - forms
            if unref_lex:
                return (Status.fails, error.format(", ".join(unref_lex)),
                        "Check whether there are missing forms.")
            return (Status.passes, "All lexemes have forms.", "")
        return (Status.NA, "(No lexemes table)", "")

    def all_cells_have_forms(self):
        error = "Not all cells have forms: {}"
        if "cells" in self.standard_tables:
            cells = set(self.get_table("cells").cell_id.to_list())
            forms = set(self.get_table("forms").cell.to_list())
            unref_cells = cells - forms
            if unref_cells:
                return (Status.fails, error.format(", ".join(unref_cells)),
                        "Check whether there are missing forms.")
            return (Status.passes, "All cells have forms.", "")
        return (Status.NA, "(No cells table)", "")

    def all_values_have_cells(self):
        error = "Not all features have cells: {}"
        if "features-values" in self.standard_tables and "cells" in self.standard_tables:
            cells = set((part
                         for cell in self.get_table("cells").cell_id.to_list()
                         for part in cell.split(".")
                         ))
            vals = set(self.get_table("features-values").value_id.to_list())
            unref_vals = vals - cells
            if unref_vals:
                return (Status.fails, error.format(", ".join(unref_vals)),
                        "Check whether there are missing cells.")
            return (Status.passes, "All feature values are present in some cells.", "")
        return (Status.NA, "(No foreign cell<->features relations)", "")

    def all_columns_have_metadata(self):
        no_metadata = []
        for r in self.p.resources:
            for col in r.schema.fields:
                if not col.description:
                    no_metadata.append(r.name + "." + col.name)
        if no_metadata:
            return (Status.fails,
                    "These columns have no detailed metadata: " + ", ".join(no_metadata),
                    "Edit the gen-metadata script to add type, description, title, and constraints.")
        return (Status.passes, "All columns have rich metadata", "")


    def tags_are_defined(self):
        taggable_tables = {"forms", "lexeme", "frequency"} & self.standard_tables

        by_tag = defaultdict(list)
        if "tags" in self.standard_tables:
            for r in self.p.get_resource("tags").read_rows():
                by_tag[r["tag_column_name"]].append(r["tag_id"])

        tags_used = False
        for tab_name in taggable_tables:
            table = self.p.get_resource(tab_name)
            tag_cols = {col for col in table.schema.field_names
                        if col.endswith("_tag")}
            if tag_cols:
                tags_used = False
                if "tags" not in self.standard_tables:
                    return (Status.fails, "Tags table missing", "Add a tags table")
        if tags_used:
            return (Status.passes, "Tags table is present", "")
        return (Status.NA, "(No tags used)", "")


    def has_vocabulary_relations(self):
        forms_table = self.p.get_resource("forms")
        missing_rels = []

        rels = [("graphemes", "grapheme_id", "forms", "orth_form"),
                ("sounds", "sound_id", "forms", "phon_form"),
                ("features-values", "value_id", "cells", "cell_id"),
                ]

        for foreign_table, identifier, table, col in rels:
            if {foreign_table, table} <= self.standard_tables \
                    and forms_table.schema.has_field(col):
                form = forms_table.schema.get_field(col)
                if not form.constraints:
                    missing_rels.append(f"{foreign_table}.{identifier} ~~~> {table}.{col}")

        if missing_rels:
            suggestion = "Re-generate metadata using the paralex package"
            return (Status.fails, "Vocabulary relation(s) missing:".format("\n\t- ".join(missing_rels)), suggestion)
        return (Status.passes, "Has vocabulary constraints", "")


    def has_doc(self):
        doc_file = list(Path(self.path).parent.glob("[Rr][Ee][Aa][Dd][Mm][Ee]*"))
        if not doc_file:
            return (Status.fails, "Could not find any readme file", "Add a readme.md")
        return (Status.passes, "Has a readme file", "")


    def has_data_sheet(self):
        data_sheet_re = "*[Dd][Aa][Tt][Aa]_[Ss][Hh][Ee][Ee][Tt]*"
        doc_file = list(Path(self.path).parent.glob(data_sheet_re))
        if not doc_file:
            doc_file = list(Path(self.path).parent.glob("docs/" + data_sheet_re))
        if not doc_file:
            return (Status.fails, "Could not find any data sheet file", "Add a data sheet!")
        return (Status.passes, "Has a data sheet file", "")


    def has_forms(self):
        exists = "forms" in set(self.p.resource_names)
        if not exists:
            return (Status.fails, "Missing forms table !", "Add a forms table")
        return (Status.passes, "Has a forms table", "")


    def has_form_triplets(self):
        forms = self.p.get_resource("forms")
        cols = set(forms.schema.field_names)
        expected = {"form_id", "lexeme", "cell"}
        one_of = {"phon_form", "orth_form"}
        if not expected <= cols and not one_of & cols:
            return (Status.fails, "Forms need to minimally define columns "
                                  "form_id, lexeme, cell, as well as either "
                                  "phon_form or orth_form.", "Add missing columns")
        return (Status.passes, "Forms table minimally defines triplets", "")


    def has_space_separated_phon_form(self):
        forms_table = self.get_table("forms")
        cols = forms_table.columns
        if "phon_form" not in cols:
            return (Status.NA, "(No phonological forms)", "")
        has_space = (forms_table["phon_form"].str.contains(" ", regex=False)
                     | (forms_table["phon_form"].str.len() <= 5))
        if not has_space.all():
            no_spaces = forms_table.loc[~has_space, :].head(5).to_markdown()
            return (Status.fails, "Phonological forms seem to not be space-separated.\n" + no_spaces,
                    "Ensure phonemes are separated by spaces.")

        return (Status.passes, "Phonological forms, if present, are space separated.", "")


    def has_coherent_analyses(self):
        forms_table = self.get_table("forms")
        cols = forms_table.columns
        if "analysed_phon_form" not in cols and "analysed_orth_form" not in cols:
            return (Status.NA, f'(No analysis columns).', '')
        analysis_rels = [("phon_form", "analysed_phon_form"),
                         ("orth_form", "analysed_orth_form"),
                         ]
        if "phon_form" in forms_table.columns:
            forms_table = forms_table[forms_table.phon_form != "#DEF#"]
        else:
            forms_table = forms_table[forms_table.orth_form != "#DEF#"]
        for form, analysis in analysis_rels:
            if form in cols and analysis in cols:
                coherent = forms_table[form].str.replace(" ", "") == \
                           forms_table[analysis].str.replace(r"[+#\s]", "", regex=True)
                if not coherent.all():
                    ex = str(forms_table[~coherent].iloc[:3, :].to_markdown())
                    return (Status.fails, f"Analyses do not seem to correspond to forms, for example: \n{ex}\n "
                                          f"Or perhaps you used custom separators ?",
                            "Make sure the forms are identical except for separators. Define separators in the docs if custom.")
        return (Status.passes, "Analyses are coherent with forms", "")


    def has_conventional_cell_ids(self):
        forms_table = self.get_table("forms")
        for c in forms_table.cell.unique():
            if not re.match(r"[a-z]([a-z\.]*[a-z]+)", c):
                return (Status.fails, f"Cell format is incorrect."
                                      f"Cells must be lowercase sequences of values, separated by dots.",
                        "Make sure the forms are identical except for separators. Define separators in the docs if custom.")
        return (Status.passes, "Cell format is correct", "")


    def is_ipa_or_has_sounds_table(self):
        if "sounds" in self.p.resource_names:
            return (Status.passes, "Defines sounds explicitly", "")

        forms = self.get_table("forms")
        cols = forms.columns
        if "phon_form" not in cols:
            return (Status.NA, "Sounds file is not necessary, there are no phon_form", "")

        ipa = ("['ɶʞ̄lɓ̃ʔç̥̜|ǁ̪̀.ʃ˞̙ɣ̟↗j̤ʙχβtɞɲz̼’eʈɤɕð̢̹ʉɦ̈ꜛʰ̰yʌˑǂɠʵɥ͡ʏɾs‿ʒ"
               "ǃʊ ̴̠̩̫̂ɝħʳʍ̊ʋʝøɽ̮œʲfæhʛrˈ˔ɗ́ŋˤɐbʁqʶˀcʼɚɯ\u2009ɨʜθx̻ʀɮ"
               "ɜo᷇ɧ̞ɢː᷅ɪ̘ɭʘɸvʐʎʴɹɘəɡdⱳʕ̽ɛ̺ʡʱ↘wˠ̆ɱ˚ɟˡɵʂꜜɳʑk̬͜ˌ̋᷄ǔʄɺʢɬⱱɖɰȁ"
               "ǀ᷆̚ɑ᷉ʷɴiʟ̯pɒmᶑɔɻ̝᷈n' ]+")

        matches = forms.phon_form.str.fullmatch(ipa)
        if not matches.all():
            return (Status.fails, "Phonological notation seems to have some custom elements, but no sounds file found.",
                    "Add a sounds file to define phonemes")
        return (Status.passes, "No sounds file, but the phon_form notation looks like IPA.")


    def has_atomic_forms(self):
        forms = self.get_table("forms")
        cols = forms.columns
        separators = r".*[;/|].*"

        if "phon_form" in cols:
            has_seps = forms.phon_form.str.fullmatch(separators).any()
            if has_seps:
                return (Status.fails, "Some phon_form values  seem to contain separators !",
                        "Use separate rows for overabundance (long form).")
        if "orth_form" in cols:
            has_seps = forms.orth_form.str.fullmatch(separators).any()
            if has_seps:
                return (Status.fails, "Some orth_form values seem to contain separators !",
                        "Use separate rows for overabundance (long form).")

        return (Status.passes, "Inflected forms seem atomic (no separators found).", "")


    def has_cell_mapping(self):
        if not "cells" in self.p.resource_names:
            return (Status.NA, "(No cells table)", "")
        cells = self.p.get_resource("cells")
        cols = set(cells.schema.field_names)
        perhaps_mappings = cols - {'cell_id', 'label', 'comment', 'POS', 'frequency', 'canonical_order'}
        if not perhaps_mappings:
            return (Status.fails, "It seems that cells are not mapped to any other vocabulary",
                    "Add mappings (eg. to UD, unimorph, other corpora schemes) to improve interoperability")
        return (Status.passes,
                "It seems that cells are mapped to other vocabularies.", "")


    def has_feature_values_mapping(self):
        if not "features-values" in self.p.resource_names:
            return (Status.NA, "(No features-values table)", "")
        values = self.p.get_resource("features-values")
        cols = set(values.schema.field_names)
        perhaps_mappings = cols - {'value_id', 'label', 'feature', 'comment', 'POS', 'canonical_order'}
        if not perhaps_mappings:
            return (Status.fails, "It seems that features are not mapped to any other vocabulary",
                    "Add mappings (eg. to UD, unimorph, other corpora schemes) to improve interoperability")
        return (Status.passes,
                "It seems that features are mapped to other vocabularies.", "")


    def has_sounds_definition(self):
        if not "sounds" in self.p.resource_names:
            return (Status.NA, "(No sounds table)", "")
        values = self.p.get_resource("sounds")
        cols = set(values.schema.field_names)
        perhaps_defs = cols - {'sound_id', 'comment'}
        if not perhaps_defs:
            return (Status.fails, "It seems that sounds are missing explicit labels or definitions.",
                    "Add a label column or map to existing vocabularies to improve interoperability")
        return (Status.passes,
                "It seems that sounds have definitions or labels.", "")


    def has_multiple_cell_mappings(self):
        if not "cells" in self.p.resource_names:
            return (Status.NA, "(No cells table)", "")
        cells = self.p.get_resource("cells")
        cols = set(cells.schema.field_names)
        perhaps_mappings = cols - {'cell_id', 'label', 'comment', 'POS', 'frequency', 'canonical_order'}
        if len(perhaps_mappings) < 2:
            return (Status.fails, "It would be better to map cells to multiple vocabularies",
                    "Add more mappings (eg. to UD, unimorph, other corpora schemes) to improve interoperability")
        return (Status.passes,
                "It seems that cells are mapped to multiple vocabularies.", "")


    def has_recommended_tables(self):
        missing = {"cells", "features-values"} - self.standard_tables
        forms = self.p.get_resource("forms")
        cols = set(forms.schema.field_names)
        if "phon_form" in cols and not "sounds" in self.standard_tables:
            missing.add("sounds")

        if missing:
            return (Status.fails, "Dataset is missing table(s): " + ", ".join(missing),
                    "Add any missing table")
        return (Status.passes, "Dataset has all recommended tables", "")


    def has_ids_first(self):
        resources = set(self.p.resource_names)
        failing = []
        for r in resources:
            table = self.p.get_resource(r)
            cols = table.schema.field_names
            if not cols[0].endswith("_id"):
                failing.append(r)
        if failing:
            return (Status.fails, "Tables where the first column isn't the id: " + ", ".join(failing),
                    "Make sure ids are present, and the first column")
        return (Status.passes, "Dataset has ids in the right place", "")


    def has_phon_form(self):
        forms = self.p.get_resource("forms")
        cols = set(forms.schema.field_names)
        if not "phon_form" in cols:
            return (Status.fails, "Forms table does not have phon_form column",
                    "Adding phonological transcriptions would make the dataset more useful for linguistic investigation.")
        return (Status.passes, "Form table has phon_form column", "")


def paralex_validation(args):
    p = ParalexValidator(args.package)
    console.rule("[bold]Paralex validation")
    console.print("\nChecking MUSTs...", style="bold")
    console.print(
        "These are mandatory: any failing statement needs to be corrected for the dataset to comply with paralex.")
    p.validate("musts")
    console.print("\nLooking for potential issues...", style="bold")
    console.print("These are indicative: failing statement indicate potential mistakes, to be checked.")
    p.validate("checks")

    console.print("\nChecking SHOULDs...", style="bold")
    console.print("These are recommendations: any failing statement indicates a potential improvement of the dataset.")
    p.validate("shoulds")
