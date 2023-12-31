import sqlite3 as sql


def setup(file):
    conn = sql.connect(file)

    cur = conn.cursor()

    create_db = "CREATE TABLE animation (characters TEXT PRIMARY KEY, img_path TEXT)"
    cur.execute(create_db)

    entries = ["INSERT INTO animation VALUES (\"a\", \"./images/aei.jpg\");",
               "INSERT INTO animation VALUES (\"b\", \"./images/bmp.jpg\");",
               "INSERT INTO animation VALUES (\"c\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"d\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"e\", \"./images/aei.jpg\");",
               "INSERT INTO animation VALUES (\"f\", \"./images/fv.jpg\");",
               "INSERT INTO animation VALUES (\"g\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"h\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"i\", \"./images/aei.jpg\");",
               "INSERT INTO animation VALUES (\"j\", \"./images/chjsh.jpg\");",
               "INSERT INTO animation VALUES (\"k\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"l\", \"./images/l.jpg\");",
               "INSERT INTO animation VALUES (\"m\", \"./images/bmp.jpg\");",
               "INSERT INTO animation VALUES (\"n\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"o\", \"./images/o.jpg\");",
               "INSERT INTO animation VALUES (\"p\", \"./images/bmp.jpg\");",
               "INSERT INTO animation VALUES (\"q\", \"./images/wq.jpg\");",
               "INSERT INTO animation VALUES (\"r\", \"./images/r.jpg\");",
               "INSERT INTO animation VALUES (\"s\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"t\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"u\", \"./images/u.jpg\");",
               "INSERT INTO animation VALUES (\"v\", \"./images/fv.jpg\");",
               "INSERT INTO animation VALUES (\"w\", \"./images/wq.jpg\");",
               "INSERT INTO animation VALUES (\"x\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"y\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"z\", \"./images/cdothers.jpg\");",
               "INSERT INTO animation VALUES (\"ch\", \"./images/chjsh.jpg\");",
               "INSERT INTO animation VALUES (\"sh\", \"./images/chjsh.jpg\");",
               "INSERT INTO animation VALUES (\"th\", \"./images/th.jpg\");",
               "INSERT INTO animation VALUES (\"NEUTRAL\", \"./images/bmp.jpg\");"
               ]

    for entry in entries:
        cur.execute(entry)

    conn.commit()

    conn.close()


def get_image_path_from_db(file, chars):
    conn = sql.connect(file)

    cur = conn.cursor()

    select_statement = f'SELECT img_path FROM animation WHERE characters = "{chars}"'
    rows = cur.execute(select_statement).fetchall()

    if len(rows) == 0:
        return -1

    return rows[0][0]


if __name__ == "__main__":
    f = "BaseAnimation.db"
    setup(f)
    print(get_image_path_from_db(f, "ch"))
