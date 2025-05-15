import pandas as pd
import hunspell

hobj = hunspell.HunSpell(
    "/usr/share/hunspell/pt_BR.dic", "/usr/share/hunspell/pt_BR.aff"
)


def is_valid_word(word):
    """
    Check if a word is valid in Portuguese using Hunspell.
    """
    return hobj.spell(word)


# Load the CSV and drop the unwanted column
df = pd.read_csv("five_letter_freq50_pt_br.csv")
df.drop(columns=["Unnamed: 0"], inplace=True)

# Filter the DataFrame
df["is_valid"] = df["word"].apply(is_valid_word)
filtered_df = df[df["is_valid"]].drop(columns=["is_valid"])

# Display or save result
print(filtered_df.info())
filtered_df.to_csv("filtered_words.csv", index=False)
