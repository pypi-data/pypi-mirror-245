import pandas as pd

other_licenses = {
    "jupyterlab": "Copyright (c) 2015-2022 Project Jupyter Contributors",
    "npm": "Copyright (c) npm, Inc. and Contributors All rights reserved.",
    "cacache": "Copyright (c) npm, Inc. and Contributors All rights reserved.",
    "err-code": "Copyright (c)",
    "eslint-plugin-prettier": "Copyright © 2017 Andres Suarez and Teddy Katz",
    "stylelint-prettier": "Copyright © 2018 Ben Scott",
    "exponential-backoff": "Copyright 2019 Coveo Solutions Inc.",
    "typescript": "Copyright (c) Microsoft Corporation. All rights reserved.",
}
licenses = pd.read_csv("./licenses.csv")

print(licenses.head())

df = pd.DataFrame(columns=["Component", "Origin", "License", "Copyright"])

for i, row in licenses.iterrows():
    copyright = "None"
    try:
        with open(f"{row['directory']}/LICENSE", "r") as f:
            for line in f.readlines():
                if "copyright" in line.lower():
                    copyright = line.strip()
                    break
    except:
        pass

    if copyright == "None":
        for key, copy in other_licenses.items():
            if key.lower() in row["name"].lower():
                copyright = copy
    elif row["name"] in other_licenses:
        copyright = other_licenses[row["name"]]

    new_row = {
        "Component": row["name"],
        "Origin": "npm",
        "License": row["from package.json"],
        "Copyright": copyright,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

df.to_csv("LICENSE-3rdparty.csv", index=False)
