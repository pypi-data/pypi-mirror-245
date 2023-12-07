from lumipy.test.unit.lumiflex_tests.utils import SqlTestCase
from lumipy.lumiflex._metadata import ColumnMeta
from lumipy.lumiflex._metadata.dtype import DType
from pydantic import ValidationError


class TestColumnMeta(SqlTestCase):

    def test_column_metadata_ctor(self):
        meta = ColumnMeta(field_name='MyCol', table_name='Test.Table', dtype=DType.Text)
        self.assertEqual('MyCol', meta.field_name)
        self.assertEqual('Test.Table', meta.table_name)
        self.assertEqual(DType.Text, meta.dtype)

    def test_column_metadata_extras_error(self):
        self.assertErrorsWithMessage(
            lambda: ColumnMeta(field_name='MyCol', table_name='Test.Table', dtype=DType.Text, bad='Value'),
            ValidationError,
            "1 validation error for ColumnMeta\nbad\n  extra fields not permitted (type=value_error.extra)"
        )

    def test_column_metadata_frozen(self):
        col = self.make_col_meta(1, True, 'test')

        def action():
            col.dtype = DType.Date,

        self.assertErrorsWithMessage(
            action,
            TypeError,
            '"ColumnMeta" is immutable and does not support item assignment',
        )

    def test_column_metadata_python_name(self):
        col_meta = ColumnMeta(field_name='MyTestColumn', table_name='Test.Table', dtype=DType.Int)
        self.assertEqual('my_test_column', col_meta.python_name())
