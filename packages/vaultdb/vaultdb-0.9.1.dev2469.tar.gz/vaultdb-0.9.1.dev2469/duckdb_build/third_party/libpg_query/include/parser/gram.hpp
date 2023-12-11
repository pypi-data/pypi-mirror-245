/* A Bison parser, made by GNU Bison 3.5.1.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2020 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Undocumented macros, especially those whose name start with YY_,
   are private implementation details.  Do not rely on them.  */

#ifndef YY_BASE_YY_THIRD_PARTY_LIBPG_QUERY_GRAMMAR_GRAMMAR_OUT_HPP_INCLUDED
# define YY_BASE_YY_THIRD_PARTY_LIBPG_QUERY_GRAMMAR_GRAMMAR_OUT_HPP_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int base_yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    IDENT = 258,
    FCONST = 259,
    SCONST = 260,
    BCONST = 261,
    XCONST = 262,
    Op = 263,
    ICONST = 264,
    PARAM = 265,
    TYPECAST = 266,
    DOT_DOT = 267,
    COLON_EQUALS = 268,
    EQUALS_GREATER = 269,
    INTEGER_DIVISION = 270,
    POWER_OF = 271,
    LAMBDA_ARROW = 272,
    DOUBLE_ARROW = 273,
    LESS_EQUALS = 274,
    GREATER_EQUALS = 275,
    NOT_EQUALS = 276,
    ABORT_P = 277,
    ABSOLUTE_P = 278,
    ACCESS = 279,
    ACTION = 280,
    ADD_P = 281,
    ADMIN = 282,
    AFTER = 283,
    AGGREGATE = 284,
    ALL = 285,
    ALSO = 286,
    ALTER = 287,
    ALWAYS = 288,
    ANALYSE = 289,
    ANALYZE = 290,
    AND = 291,
    ANTI = 292,
    ANY = 293,
    ARRAY = 294,
    AS = 295,
    ASC_P = 296,
    ASOF = 297,
    ASSERTION = 298,
    ASSIGNMENT = 299,
    ASYMMETRIC = 300,
    AT = 301,
    ATTACH = 302,
    ATTRIBUTE = 303,
    AUTHORIZATION = 304,
    BACKWARD = 305,
    BEFORE = 306,
    BEGIN_P = 307,
    BETWEEN = 308,
    BIGINT = 309,
    BINARY = 310,
    BIT = 311,
    BOOLEAN_P = 312,
    BOTH = 313,
    BY = 314,
    CACHE = 315,
    CALL_P = 316,
    CALLED = 317,
    CASCADE = 318,
    CASCADED = 319,
    CASE = 320,
    CAST = 321,
    CATALOG_P = 322,
    CENTURIES_P = 323,
    CENTURY_P = 324,
    CHAIN = 325,
    CHAR_P = 326,
    CHARACTER = 327,
    CHARACTERISTICS = 328,
    CHECK_P = 329,
    CHECKPOINT = 330,
    CLASS = 331,
    CLOSE = 332,
    CLUSTER = 333,
    COALESCE = 334,
    COLLATE = 335,
    COLLATION = 336,
    COLUMN = 337,
    COLUMNS = 338,
    COMMENT = 339,
    COMMENTS = 340,
    COMMIT = 341,
    COMMITTED = 342,
    COMPRESSION = 343,
    CONCURRENTLY = 344,
    CONFIG = 345,
    CONFIGURATION = 346,
    CONFLICT = 347,
    CONNECTION = 348,
    CONSTRAINT = 349,
    CONSTRAINTS = 350,
    CONTENT_P = 351,
    CONTINUE_P = 352,
    CONVERSION_P = 353,
    COPY = 354,
    COST = 355,
    CREATE_P = 356,
    CROSS = 357,
    CSV = 358,
    CUBE = 359,
    CURRENT_P = 360,
    CURSOR = 361,
    CYCLE = 362,
    DATA_P = 363,
    DATABASE = 364,
    DAY_P = 365,
    DAYS_P = 366,
    DEALLOCATE = 367,
    DEC = 368,
    DECADE_P = 369,
    DECADES_P = 370,
    DECIMAL_P = 371,
    DECLARE = 372,
    DEFAULT = 373,
    DEFAULTS = 374,
    DEFERRABLE = 375,
    DEFERRED = 376,
    DEFINER = 377,
    DELETE_P = 378,
    DELIMITER = 379,
    DELIMITERS = 380,
    DEPENDS = 381,
    DESC_P = 382,
    DESCRIBE = 383,
    DETACH = 384,
    DICTIONARY = 385,
    DISABLE_P = 386,
    DISCARD = 387,
    DISTINCT = 388,
    DO = 389,
    DOCUMENT_P = 390,
    DOMAIN_P = 391,
    DOUBLE_P = 392,
    DROP = 393,
    EACH = 394,
    ELSE = 395,
    ENABLE_P = 396,
    ENCODING = 397,
    ENCRYPTED = 398,
    END_P = 399,
    ENUM_P = 400,
    ESCAPE = 401,
    EVENT = 402,
    EXCEPT = 403,
    EXCLUDE = 404,
    EXCLUDING = 405,
    EXCLUSIVE = 406,
    EXECUTE = 407,
    EXISTS = 408,
    EXPLAIN = 409,
    EXPORT_P = 410,
    EXPORT_STATE = 411,
    EXTENSION = 412,
    EXTERNAL = 413,
    EXTRACT = 414,
    FALSE_P = 415,
    FAMILY = 416,
    FETCH = 417,
    FILTER = 418,
    FIRST_P = 419,
    FLOAT_P = 420,
    FOLLOWING = 421,
    FOR = 422,
    FORCE = 423,
    FOREIGN = 424,
    FORTRESS = 425,
    FORWARD = 426,
    FREEZE = 427,
    FROM = 428,
    FULL = 429,
    FUNCTION = 430,
    FUNCTIONS = 431,
    GENERATED = 432,
    GLOB = 433,
    GLOBAL = 434,
    GRANT = 435,
    GRANTED = 436,
    GROUP_P = 437,
    GROUPING = 438,
    GROUPING_ID = 439,
    GROUPS = 440,
    HANDLER = 441,
    HAVING = 442,
    HEADER_P = 443,
    HOLD = 444,
    HOUR_P = 445,
    HOURS_P = 446,
    IDENTITY_P = 447,
    IF_P = 448,
    IGNORE_P = 449,
    ILIKE = 450,
    IMMEDIATE = 451,
    IMMUTABLE = 452,
    IMPLICIT_P = 453,
    IMPORT_P = 454,
    IN_P = 455,
    INCLUDE_P = 456,
    INCLUDING = 457,
    INCREMENT = 458,
    INDEX = 459,
    INDEXES = 460,
    INHERIT = 461,
    INHERITS = 462,
    INITIALLY = 463,
    INLINE_P = 464,
    INNER_P = 465,
    INOUT = 466,
    INPUT_P = 467,
    INSENSITIVE = 468,
    INSERT = 469,
    INSTALL = 470,
    INSTEAD = 471,
    INT_P = 472,
    INTEGER = 473,
    INTERSECT = 474,
    INTERVAL = 475,
    INTO = 476,
    INVOKER = 477,
    IS = 478,
    ISNULL = 479,
    ISOLATION = 480,
    JOIN = 481,
    JSON = 482,
    KEY = 483,
    LABEL = 484,
    LANGUAGE = 485,
    LARGE_P = 486,
    LAST_P = 487,
    LATERAL_P = 488,
    LEADING = 489,
    LEAKPROOF = 490,
    LEFT = 491,
    LEVEL = 492,
    LIKE = 493,
    LIMIT = 494,
    LISTEN = 495,
    LOAD = 496,
    LOCAL = 497,
    LOCATION = 498,
    LOCK_P = 499,
    LOCKED = 500,
    LOGGED = 501,
    LOGIN = 502,
    MACRO = 503,
    MAP = 504,
    MAPPING = 505,
    MATCH = 506,
    MATERIALIZED = 507,
    MAXVALUE = 508,
    MERGE_P = 509,
    METHOD = 510,
    MICROSECOND_P = 511,
    MICROSECONDS_P = 512,
    MILLENNIA_P = 513,
    MILLENNIUM_P = 514,
    MILLISECOND_P = 515,
    MILLISECONDS_P = 516,
    MINUTE_P = 517,
    MINUTES_P = 518,
    MINVALUE = 519,
    MODE = 520,
    MONTH_P = 521,
    MONTHS_P = 522,
    MOVE = 523,
    NAME_P = 524,
    NAMES = 525,
    NATIONAL = 526,
    NATURAL = 527,
    NCHAR = 528,
    NEW = 529,
    NEXT = 530,
    NO = 531,
    NOLOGIN = 532,
    NONE = 533,
    NOSUPERUSER = 534,
    NOT = 535,
    NOTHING = 536,
    NOTIFY = 537,
    NOTNULL = 538,
    NOWAIT = 539,
    NULL_P = 540,
    NULLIF = 541,
    NULLS_P = 542,
    NUMERIC = 543,
    OBJECT_P = 544,
    OF = 545,
    OFF = 546,
    OFFSET = 547,
    OIDS = 548,
    OLD = 549,
    ON = 550,
    ONLY = 551,
    OPERATOR = 552,
    OPTION = 553,
    OPTIONS = 554,
    OR = 555,
    ORDER = 556,
    ORDINALITY = 557,
    OTHERS = 558,
    OUT_P = 559,
    OUTER_P = 560,
    OVER = 561,
    OVERLAPS = 562,
    OVERLAY = 563,
    OVERRIDING = 564,
    OWNED = 565,
    OWNER = 566,
    PARALLEL = 567,
    PARSER = 568,
    PARTIAL = 569,
    PARTITION = 570,
    PASSING = 571,
    PASSWORD = 572,
    PERCENT = 573,
    PIVOT = 574,
    PIVOT_LONGER = 575,
    PIVOT_WIDER = 576,
    PLACING = 577,
    PLANS = 578,
    POLICY = 579,
    POSITION = 580,
    POSITIONAL = 581,
    PRAGMA_P = 582,
    PRECEDING = 583,
    PRECISION = 584,
    PREPARE = 585,
    PREPARED = 586,
    PRESERVE = 587,
    PRIMARY = 588,
    PRIOR = 589,
    PRIVILEGES = 590,
    PROCEDURAL = 591,
    PROCEDURE = 592,
    PROGRAM = 593,
    PUBLICATION = 594,
    PUSH_P = 595,
    QUALIFY = 596,
    QUOTE = 597,
    RANGE = 598,
    READ_P = 599,
    REAL = 600,
    REASSIGN = 601,
    RECHECK = 602,
    RECURSIVE = 603,
    REF = 604,
    REFERENCES = 605,
    REFERENCING = 606,
    REFRESH = 607,
    REINDEX = 608,
    RELATIVE_P = 609,
    RELEASE = 610,
    REMOTE = 611,
    REMOTE_MERGE_PATH = 612,
    RENAME = 613,
    REPEATABLE = 614,
    REPLACE = 615,
    REPLICA = 616,
    RESET = 617,
    RESPECT_P = 618,
    RESTART = 619,
    RESTRICT = 620,
    RETURNING = 621,
    RETURNS = 622,
    REVOKE = 623,
    RIGHT = 624,
    ROLE = 625,
    ROLLBACK = 626,
    ROLLUP = 627,
    ROW = 628,
    ROWS = 629,
    RULE = 630,
    SAMPLE = 631,
    SAVEPOINT = 632,
    SCHEMA = 633,
    SCHEMAS = 634,
    SCROLL = 635,
    SEARCH = 636,
    SECOND_P = 637,
    SECONDS_P = 638,
    SECURITY = 639,
    SELECT = 640,
    SEMI = 641,
    SEQUENCE = 642,
    SEQUENCES = 643,
    SERIALIZABLE = 644,
    SERVER = 645,
    SESSION = 646,
    SET = 647,
    SETOF = 648,
    SETS = 649,
    SHARE = 650,
    SHOW = 651,
    SIMILAR = 652,
    SIMPLE = 653,
    SKIP = 654,
    SMALLINT = 655,
    SNAPSHOT = 656,
    SOME = 657,
    SQL_P = 658,
    STABLE = 659,
    STANDALONE_P = 660,
    START = 661,
    STATEMENT = 662,
    STATISTICS = 663,
    STDIN = 664,
    STDOUT = 665,
    STORAGE = 666,
    STORED = 667,
    STRICT_P = 668,
    STRIP_P = 669,
    STRUCT = 670,
    SUBSCRIPTION = 671,
    SUBSTRING = 672,
    SUMMARIZE = 673,
    SUPERUSER = 674,
    SYMMETRIC = 675,
    SYSID = 676,
    SYSTEM_P = 677,
    TABLE = 678,
    TABLES = 679,
    TABLESAMPLE = 680,
    TABLESPACE = 681,
    TAG = 682,
    TEMP = 683,
    TEMPLATE = 684,
    TEMPORARY = 685,
    TEXT_P = 686,
    THEN = 687,
    TIES = 688,
    TIME = 689,
    TIMESTAMP = 690,
    TO = 691,
    TRAILING = 692,
    TRANSACTION = 693,
    TRANSFORM = 694,
    TREAT = 695,
    TRIGGER = 696,
    TRIM = 697,
    TRUE_P = 698,
    TRUNCATE = 699,
    TRUSTED = 700,
    TRY_CAST = 701,
    TYPE_P = 702,
    TYPES_P = 703,
    UNBOUNDED = 704,
    UNCOMMITTED = 705,
    UNENCRYPTED = 706,
    UNION = 707,
    UNIQUE = 708,
    UNKNOWN = 709,
    UNLISTEN = 710,
    UNLOCK = 711,
    UNLOGGED = 712,
    UNPIVOT = 713,
    UNTIL = 714,
    UPDATE = 715,
    USE_P = 716,
    USER = 717,
    USING = 718,
    VACUUM = 719,
    VALID = 720,
    VALIDATE = 721,
    VALIDATOR = 722,
    VALUE_P = 723,
    VALUES = 724,
    VARCHAR = 725,
    VARIADIC = 726,
    VARYING = 727,
    VERBOSE = 728,
    VERSION_P = 729,
    VIEW = 730,
    VIEWS = 731,
    VIRTUAL = 732,
    VOLATILE = 733,
    WEEK_P = 734,
    WEEKS_P = 735,
    WHEN = 736,
    WHERE = 737,
    WHITESPACE_P = 738,
    WINDOW = 739,
    WITH = 740,
    WITHIN = 741,
    WITHOUT = 742,
    WORK = 743,
    WRAPPER = 744,
    WRITE_P = 745,
    XML_P = 746,
    XMLATTRIBUTES = 747,
    XMLCONCAT = 748,
    XMLELEMENT = 749,
    XMLEXISTS = 750,
    XMLFOREST = 751,
    XMLNAMESPACES = 752,
    XMLPARSE = 753,
    XMLPI = 754,
    XMLROOT = 755,
    XMLSERIALIZE = 756,
    XMLTABLE = 757,
    YEAR_P = 758,
    YEARS_P = 759,
    YES_P = 760,
    ZONE = 761,
    NOT_LA = 762,
    NULLS_LA = 763,
    WITH_LA = 764,
    POSTFIXOP = 765,
    UMINUS = 766
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 14 "third_party/libpg_query/grammar/grammar.y"

	core_YYSTYPE		core_yystype;
	/* these fields must match core_YYSTYPE: */
	int					ival;
	char				*str;
	const char			*keyword;
	const char          *conststr;

	char				chr;
	bool				boolean;
	PGJoinType			jtype;
	PGDropBehavior		dbehavior;
	PGOnCommitAction		oncommit;
	PGOnCreateConflict		oncreateconflict;
	PGList				*list;
	PGNode				*node;
	PGValue				*value;
	PGObjectType			objtype;
	PGTypeName			*typnam;
	PGObjectWithArgs		*objwithargs;
	PGDefElem				*defelt;
	PGSortBy				*sortby;
	PGWindowDef			*windef;
	PGJoinExpr			*jexpr;
	PGIndexElem			*ielem;
	PGAlias				*alias;
	PGRangeVar			*range;
	PGIntoClause			*into;
	PGCTEMaterialize			ctematerialize;
	PGWithClause			*with;
	PGInferClause			*infer;
	PGOnConflictClause	*onconflict;
	PGOnConflictActionAlias onconflictshorthand;
	PGAIndices			*aind;
	PGResTarget			*target;
	PGInsertStmt			*istmt;
	PGVariableSetStmt		*vsetstmt;
	PGOverridingKind       override;
	PGSortByDir            sortorder;
	PGSortByNulls          nullorder;
	PGConstrType           constr;
	PGLockClauseStrength lockstrength;
	PGLockWaitPolicy lockwaitpolicy;
	PGSubLinkType subquerytype;
	PGViewCheckOption viewcheckoption;
	PGInsertColumnOrder bynameorposition;

#line 617 "third_party/libpg_query/grammar/grammar_out.hpp"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif



int base_yyparse (core_yyscan_t yyscanner);

#endif /* !YY_BASE_YY_THIRD_PARTY_LIBPG_QUERY_GRAMMAR_GRAMMAR_OUT_HPP_INCLUDED  */
