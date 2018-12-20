CREATE TABLE parametros(
  parametro varchar(100) NOT NULL COMMENT 'Sigla/Nome do parametro',
  descricao varchar(100) DEFAULT NULL COMMENT 'Descricao resumida do parametro',
  valor varchar(100) NOT NULL,
  UNIQUE KEY parametro (parametro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;