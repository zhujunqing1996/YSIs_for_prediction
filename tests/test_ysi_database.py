import os

import pandas as pd
import pytest
import rdkit.Chem

dir_path = os.path.dirname(os.path.realpath(__file__))
ysi_path = os.path.join(dir_path, os.pardir, 'ysi.csv')


@pytest.fixture
def ysis():
    return pd.read_csv(ysi_path)


def ysis_exist():
    assert os.path.exists(ysi_path)


def test_ysi_columns(ysis):
    assert set(ysis.columns) == {'Species', 'CAS', 'Type', 'SMILES', 'YSI', 'YSI_err'}


def test_smiles_canonical(ysis):
    valid_smiles = (ysis.SMILES == ysis.SMILES.apply(rdkit.Chem.CanonSmiles))
    assert valid_smiles.all(), f"Issue with {ysis[~valid_smiles]} not having canonical smiles"


def test_duplciates(ysis):
    ysis['SMILES'] = ysis.SMILES.apply(rdkit.Chem.CanonSmiles)
    duplicated = ysis.SMILES.duplicated()
    assert not duplicated.any(), f"Duplicates found: {ysis[duplicated]}"
