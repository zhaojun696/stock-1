use gp;

-- auto-generated definition
drop table if exists kline_day  ;
create table kline_day
(
   id bigint(20) primary key NOT NULL AUTO_INCREMENT COMMENT '主键',
   code varchar(20) not null default '' comment '股票代码',
   open double comment '开盘价',
   close double comment '收盘价',
   high double comment '最高价',
   low double comment '最低价',
   turnover_volume double comment '成交量',
   turnover_ratio double comment '换手率',
   ma5 double comment '5日均线',
   ma10 double comment '10日均线',
   ma20 double comment '20日均线',
   ma60 double comment '60日均线',
   day date comment '日期'

) charset=utf8;


drop table if exists kline_week  ;
create table kline_week
(
    id bigint(20) primary key NOT NULL AUTO_INCREMENT COMMENT '主键',
    code varchar(20) not null default '' comment '股票代码',
    open double comment '开盘价',
    close double comment '收盘价',
    high double comment '最高价',
    low double comment '最低价',
    turnover_volume double comment '成交量',
    turnover_ratio double comment '换手率',
    ma5 double comment '5日均线',
    ma10 double comment '10日均线',
    ma20 double comment '20日均线',
    ma60 double comment '60日均线',
    week date comment '日期'

) charset=utf8;


drop table if exists zixuan  ;
create table zixuan
(
    id bigint(20) primary key NOT NULL AUTO_INCREMENT COMMENT '主键',
    code varchar(20) not null default '' comment '股票代码',
    weight int not null  default 50 comment '权重',
    hot_rel_percent int not null default 50 comment '热点关联度'

) charset=utf8;


