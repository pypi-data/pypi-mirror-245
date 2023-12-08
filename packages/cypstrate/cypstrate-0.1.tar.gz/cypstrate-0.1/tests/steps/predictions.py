import pandas as pd
from pytest_bdd import parsers, then, when


@when(
    parsers.parse("the model generates predictions for the molecule representations"),
    target_fixture="predictions",
)
def predictions(representations, model, input_type, prediction_mode):
    if input_type == "smiles":
        return model.predict_smiles(representations, prediction_mode=prediction_mode)
    elif input_type == "mol_block":
        return model.predict_mol_blocks(
            representations, prediction_mode=prediction_mode
        )
    elif input_type == "rdkit_mol":
        return model.predict_mols(representations, prediction_mode=prediction_mode)
    else:
        raise ValueError(f"Unknown input_type: {input_type}")


@when(
    "The subset of the result where the input was not None is considered",
    target_fixture="subset",
)
def subset_without_none(predictions):
    # remove None entries
    return predictions[predictions.input_mol.notnull()]


@then("the result should be a pandas DataFrame")
def check_result(predictions):
    assert isinstance(predictions, pd.DataFrame)
