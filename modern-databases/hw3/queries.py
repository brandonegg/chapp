class QueryBuilder:
  def __init__(self):
    self.query = ''
    self.use_and = False

  def delete(self, table):
    self.query += f"DELETE FROM {table}"

  def select(self, table, columns: list | str):
    if type(columns) == list:
      columns = ','.join(columns)

    self.query += f"SELECT {columns} FROM {table}"

  def where(self, condition: str):
    '''
    This will conditionally handle multiple where clauses,
    appending following where's with AND
    '''
    base = 'WHERE'
    if self.use_and:
      base = 'AND'

    self.use_and = True

    self.query += f" {base} {condition}"
    
  def end(self):
    return self.query