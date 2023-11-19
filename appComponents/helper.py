def medal_telly(df):

    medal_telly = df.drop_duplicates(subset=['Team', "NOC", "Games", "Year",
                                             "City", "Sport", "Event", "Medal"])

    medal_telly = medal_telly.groupby("region").sum()[["Gold", "Silver", "Bronze"]].sort_values(
        by="Gold", ascending=False).reset_index()

    medal_telly["total"] = medal_telly["Bronze"] + \
        medal_telly["Silver"] + medal_telly["Gold"]

    return medal_telly
