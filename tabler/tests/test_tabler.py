import os

from tabler import CSV, HTML, ODS, XLSX, Table, ToHTML

import pytest


@pytest.fixture
def table():
    header = ['Col1', 'Col2', 'Col3']
    data = [['Red', 'Green', 'Blue'], ['Orange', 'Yellow', 'Magenta']]
    return Table(header=header, data=data)


@pytest.fixture
def test_csv_path():
    return str(os.path.join(os.path.dirname(__file__), 'testfile.csv'))


@pytest.fixture
def test_ods_path():
    return str(os.path.join(os.path.dirname(__file__), 'testfile.ods'))


@pytest.fixture
def test_xlsx_path():
    return str(os.path.join(os.path.dirname(__file__), 'testfile.xlsx'))


def test_create_table_with_header_and_data(table):
    assert len(table.header) == 3
    assert len(table) == 2
    assert all([len(row) == 3 for row in table])


def test_create_table_no_args_raises_valueerror():
    with pytest.raises(ValueError):
        Table()


def test_access_cell_by_header_column_index(table):
    assert table[0][0] == 'Red'


def test_access_cell_by_header_name_column_index(table):
    assert table[0]['Col1'] == 'Red'


def test_change_cell_value(table):
    assert table[0]['Col1'] == 'Red'
    table[0]['Col1'] = 'Green'
    assert table[0]['Col1'] == 'Green'


def test_get_table_column(table):
    assert table.get_column('Col1') == ['Red', 'Orange']


def open_table(filename, table_type):
    return Table(filename, table_type=table_type)


def test_open_csv(test_csv_path):
    open_table(test_csv_path, CSV())


def test_open_ods(test_ods_path):
    open_table(test_ods_path, ODS())


def test_open_xlsx(test_xlsx_path):
    open_table(test_xlsx_path, XLSX())


def save_table(filename, table_type, table, tmpdir):
    path = str(tmpdir.join(filename))
    table.write(filepath=path, table_type=table_type)
    assert os.path.exists(path)


def test_save_csv_file(table, tmpdir):
    save_table('testfile.csv', CSV(), table, tmpdir)


def test_save_ods_file(table, tmpdir):
    save_table('testfile.ods', ODS(), table, tmpdir)


def test_save_xlsx_file(table, tmpdir):
    save_table('testfile.xlsx', XLSX(), table, tmpdir)


def test_save_html_file(table, tmpdir):
    save_table('testfile.html', HTML(), table, tmpdir)


def test_open_file_without_table_type(test_csv_path):
    Table(test_csv_path)


def test_save_file_without_extension(table, tmpdir):
    filename = 'testfile'
    path = str(tmpdir.join(filename))
    table.write(filepath=path, table_type=CSV())
    assert os.path.exists(path + '.csv')


def test_save_file_without_table_type(table, tmpdir):
    filename = 'testfile.csv'
    path = str(tmpdir.join(filename))
    table.write(filepath=path)
    assert os.path.exists(path)
