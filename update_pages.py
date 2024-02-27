#!/usr/bin/env python
# coding: utf-8

import re
import pandas as pd
import numpy as np
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


# Divide the countries into their zones
# Data taken from FIE.org dropdown at https://fie.org/fie/structure/federations-map

regex = re.compile(r'<option value="([A-Z_]*)">(.*)</option>')
zones = {}

country_strings = {}
country_strings["Africa"] = """<option value="ALG">ALGERIA</option><option value="ANG">ANGOLA</option><option value="BEN">BENIN</option><option value="BOT">BOTSWANA</option><option value="BUR">BURKINA FASO</option><option value="CMR">CAMEROON</option><option value="CPV">CAPE VERDE </option><option value="CGO">CONGO</option><option value="CIV">COTE D'IVOIRE</option><option value="COD">DEMOCRATIC REPUBLIC OF CONGO</option><option value="EGY">EGYPT</option><option value="GHA">GHANA</option><option value="GUI">GUINEA</option><option value="KEN">KENYA</option><option value="LBA">LIBYA</option><option value="MAD">MADAGASCAR</option><option value="MLI">MALI</option><option value="MTN">MAURITANIA</option><option value="MRI">MAURITIUS</option><option value="MAR">MOROCCO</option><option value="NAM">NAMIBIA</option><option value="NIG">NIGER</option><option value="NGR">NIGERIA</option><option value="RWA">RWANDA</option><option value="SEN">SENEGAL</option><option value="SLE">SIERRA LEONE</option><option value="RSA">SOUTH AFRICA</option><option value="TOG">TOGO</option><option value="TUN">TUNISIA</option><option value="UGA">UGANDA</option>"""
country_strings["Americas"] = """<option value="ANT">ANTIGUA AND BARBUDA</option><option value="ARG">ARGENTINA</option><option value="ARU">ARUBA</option><option value="BAH">BAHAMAS</option><option value="BAR">BARBADOS</option><option value="BIZ">BELIZE</option><option value="BER">BERMUDA</option><option value="BOL">BOLIVIA</option><option value="BRA">BRAZIL</option><option value="CAN">CANADA</option><option value="CHI">CHILE</option><option value="COL">COLOMBIA</option><option value="CRC">COSTA RICA</option><option value="CUB">CUBA</option><option value="DMA">DOMINICA</option><option value="DOM">DOMINICAN REPUBLIC</option><option value="ECU">ECUADOR</option><option value="ESA">EL SALVADOR</option><option value="GUA">GUATEMALA</option><option value="GUY">GUYANA</option><option value="HAI">HAITI</option><option value="HON">HONDURAS</option><option value="JAM">JAMAICA</option><option value="MEX">MEXICO</option><option value="NCA">NICARAGUA</option><option value="PAN">PANAMA</option><option value="PAR">PARAGUAY</option><option value="PER">PERU</option><option value="PUR">PUERTO RICO</option><option value="URU">URUGUAY</option><option value="USA">USA</option><option value="VEN">VENEZUELA</option><option value="ISV">VIRGIN ISLANDS</option>"""
country_strings["Europe"] = """<option value="MNE">MONTENEGRO</option><option value="_AIN">_AIN</option><option value="AIN_">AIN_</option><option value="ARM">ARMENIA</option><option value="AUT">AUSTRIA</option><option value="AZE">AZERBAIJAN</option><option value="BLR">BELARUS</option><option value="BEL">BELGIUM</option><option value="BUL">BULGARIA</option><option value="CRO">CROATIA</option><option value="CYP">CYPRUS</option><option value="CZE">CZECH REPUBLIC</option><option value="DEN">DENMARK</option><option value="EST">ESTONIA</option><option value="FIN">FINLAND</option><option value="FRA">FRANCE</option><option value="GEO">GEORGIA</option><option value="GER">GERMANY</option><option value="GBR">GREAT BRITAIN</option><option value="GRE">GREECE</option><option value="HUN">HUNGARY</option><option value="ISL">ICELAND</option><option value="IRL">IRELAND</option><option value="ISR">ISRAEL</option><option value="ITA">ITALY</option><option value="LAT">LATVIA</option><option value="LTU">LITHUANIA</option><option value="LUX">LUXEMBOURG</option><option value="MLT">MALTA</option><option value="MDA">MOLDOVA</option><option value="MON">MONACO</option><option value="NED">NETHERLANDS</option><option value="MKD">NORTH MACEDONIA</option><option value="NOR">NORWAY</option><option value="POL">POLAND</option><option value="POR">PORTUGAL</option><option value="ROU">ROMANIA</option><option value="RUS">RUSSIA</option><option value="SMR">SAN MARINO</option><option value="SRB">SERBIA</option><option value="SVK">SLOVAKIA</option><option value="SLO">SLOVENIA</option><option value="ESP">SPAIN</option><option value="SWE">SWEDEN</option><option value="SUI">SWITZERLAND</option><option value="TUR">TÜRKIYE</option><option value="UKR">UKRAINE</option>"""
country_strings["Asia"] = """<option value="AFG">AFGHANISTAN</option><option value="ASA">AMERICAN SAMOA</option><option value="AUS">AUSTRALIA</option><option value="BRN">BAHRAIN</option><option value="BAN">BANGLADESH</option><option value="BRU">BRUNEI DARUSSALAM</option><option value="CAM">CAMBODIA</option><option value="CHN">CHINA</option><option value="TPE">CHINESE TAIPEI</option><option value="GUM">GUAM</option><option value="HKG">HONG KONG, CHINA</option><option value="IND">INDIA</option><option value="INA">INDONESIA</option><option value="IRI">IRAN</option><option value="IRQ">IRAQ</option><option value="JPN">JAPAN</option><option value="JOR">JORDAN</option><option value="KAZ">KAZAKHSTAN</option><option value="KOR">KOREA</option><option value="KUW">KUWAIT</option><option value="KGZ">KYRGYZSTAN</option><option value="LBN">LEBANON</option><option value="MAC">MACAO, CHINA</option><option value="MAS">MALAYSIA</option><option value="MGL">MONGOLIA</option><option value="MYA">MYANMAR</option><option value="NEP">NEPAL</option><option value="NZL">NEW ZEALAND</option><option value="PRK">NORTH KOREA</option><option value="OMA">OMAN</option><option value="PAK">PAKISTAN</option><option value="PLE">PALESTINE</option><option value="PNG">PAPUA NEW GUINEA</option><option value="PHI">PHILIPPINES</option><option value="QAT">QATAR</option><option value="SAM">SAMOA</option><option value="KSA">SAUDI ARABIA</option><option value="SGP">SINGAPORE</option><option value="SRI">SRI LANKA</option><option value="SYR">SYRIAN ARAB REPUBLIC</option><option value="TJK">TAJIKISTAN</option><option value="THA">THAILAND</option><option value="TKM">TURKMENISTAN</option><option value="UAE">UNITED ARAB EMIRATES</option><option value="UZB">UZBEKISTAN</option><option value="VIE">VIETNAM</option><option value="YEM">YEMEN</option>"""

for key, country_string in country_strings.items():
    country_string = country_string.replace("><", ">\n<")
    country_string = country_string.split("\n")

    countries = {}
    for x in country_string:
        result = re.search(regex, x)
        abbr, country = result.groups()
        countries[abbr] = country
    
    zones[key] = list(countries.keys())


# Constants and Functions

creation_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
qualification_start = datetime(2023, 4, 3)
constant_columns = ["Name", "Country"]

weapons = {"S": "Sabre", "E": "Epee", "F": "Foil"}
genders = {"M": "Men", "W": "Women"}

def convert_string_to_points(tmp):
    if isinstance(tmp, int) or isinstance(tmp, float):
        if np.isnan(tmp):
            return 0
        else:
            return float(tmp)
    tmp = tmp.replace("+", "")
    if tmp.startswith("(") and tmp.endswith(")"):
        tmp = tmp[1: -1]
    tmp = float(tmp)
    return(tmp)

def convert_country_to_zone(abbreviation):
    for key, countries in zones.items():
        if abbreviation in countries:
            return(key)
    raise NotImplementedError(f"The country {abbreviation} is missing from the zones list.")

def fie_ranking(gender, weapon, event):
    return(f"https://fie.org/athletes/general-ranks/?category=S&weapon={weapon}&gender={gender}&event={event}&season=2024")


# Qualification for each discipline

for weapon_key, weapon_label in weapons.items():
    for gender_key, gender_label in genders.items():
        # Read data
        tables = {
            "individual": pd.read_html(fie_ranking(gender_key, weapon_key, "I"))[0],
            "team": pd.read_html(fie_ranking(gender_key, weapon_key, "E"))[0],
        }

        # Cleanup and preprocess data
        competition_columns = {}
        contributing_competitions_columns = {}

        for label in tables.keys():
            table = tables[label]
            table = table.drop(columns=["Unnamed: 0", "Total"])

            table = table.rename(columns={table.columns[0]: constant_columns[0],
                                      table.columns[1]: constant_columns[1]})

            competition_columns[label] = [column for column in table.columns if column not in constant_columns]
            contributing_competitions_columns[label] = []

            for column in competition_columns[label]:
                table[column] = table[column].apply(convert_string_to_points)

                day, month, year = [int(x) for x in column.split()[0].split(".")]

                competition_date = datetime(year+2000, month, day)
                if qualification_start < competition_date:
                    contributing_competitions_columns[label].append(column)

            table["Zone"] = table["Country"].apply(convert_country_to_zone)

            max_events = 6 if label == "team" else 7

            if len(contributing_competitions_columns[label]) > max_events:
                datavalues = table[contributing_competitions_columns[label]].values
                table["Total"] = np.sum(np.partition(datavalues, -max_events)[:, -max_events:], 1)
            else:
                table["Total"] = table[contributing_competitions_columns[label]].sum(axis=1)
            tables[label] = table
        
        
        
        # Qualification
        for label in tables.keys():
            table = tables[label]
            table = table.sort_values("Total", ascending=False)
            table["Qualified"] = 0
            table = table.reset_index(drop=True)
            tables[label] = table

        column_qualified_team = tables["team"].columns.get_loc("Qualified")
        column_qualified_individual = tables["individual"].columns.get_loc("Qualified")

        # Top 4 Teams are qualified
        qualified_teams = list(tables["team"]["Country"].head(4).values)
        qualified_teams_names = list(tables["team"]["Name"].head(4).values)
        tables["team"].iloc[:4, column_qualified_team] = 1

        # Best Team from each zone in 5-16 is qualified
        view_5to16 = tables["team"].iloc[4:16]
        mask = ~(view_5to16.duplicated(subset="Zone", keep="first"))
        indices = view_5to16.loc[mask, "Qualified"].index
        tables["team"].iloc[indices, column_qualified_team] = 2

        qualified_teams.extend(tables["team"].iloc[indices]["Country"].values)
        qualified_teams_names.extend(tables["team"].iloc[indices]["Name"].values)
        

        # Fill up with teams till 8 teams are reached
        teams_to_fill = 8 - len(qualified_teams)
        mask = (tables["team"]["Qualified"] == 0)

        indices = tables["team"][mask].index
        indices = indices[:teams_to_fill]

        qualified_teams.extend(tables["team"].iloc[indices]["Country"].values)
        qualified_teams_names.extend(tables["team"].iloc[indices]["Name"].values)
        
        tables["team"].iloc[indices, column_qualified_team] = 3

        # Individual Qualifying
        qualified_individuals = []
        tables["individual"]["Qualified"] = tables["individual"]["Country"].apply(lambda x: x in qualified_teams)
        tables["individual"]["Qualified"] *= -1
        
        # Create a mask if fencers are in Top 4 of their country, if so set Qualified to 1, otherwise to -1
        fencers_qualified_via_team = tables["individual"].groupby("Country").head(4).index
        tables["individual"].iloc[fencers_qualified_via_team, column_qualified_individual] *= -1
        
        # Get best 2 from Europe, best 2 from Asia, 1 from Americas, 1 from Africa
        individual_places = {
            "Europe": 2,
            "Asia": 2,
            "Americas": 1,
            "Africa": 1,
        }

        for zone, places in individual_places.items():
            # Create a mask that only keeps the top fencer from each nation
            mask = ~(tables["individual"].duplicated(subset="Country", keep="first"))
            view = tables["individual"][mask].query("Zone == @zone and Qualified == 0")

            indices = view.index[:places]
            qualified_individuals.extend(tables["individual"].iloc[indices]["Name"].values)
            tmp_countries = tables["individual"].iloc[indices]["Country"].values
            
            # Invalidate all other fencers from this nation and validate the top fencers
            indices_countrymen = tables["individual"].query("Country in @tmp_countries").index
            tables["individual"].iloc[indices_countrymen, column_qualified_individual] = -2
            tables["individual"].iloc[indices, column_qualified_individual] = 2
        
            

         # List fencers going to the zonal qualification tournaments
        
        fencers_zonals = {}
        for zone in individual_places.keys():
            view = tables["individual"].query("Zone == @zone and Qualified == 0")
            mask = ~(view.duplicated(subset="Country", keep="first"))
            indices = view[mask].index
            fencers_zonals[zone] = view[mask]["Name"].values
            tables["individual"].iloc[indices, column_qualified_individual] = 4
            
        # Create Templates for Website
        template_name = "template_results.html"
        jinja_dict = {
            "tables": tables,
            "gender_label": gender_label,
            "weapon_label": weapon_label,
            "ranking_individual": tables["individual"],
            "ranking_individual_columns": ["Name", "Country", "Total"] + contributing_competitions_columns["individual"],
            "ranking_team": tables["team"],
            "ranking_team_columns": ["Name", "Total"] + contributing_competitions_columns["team"],
            "creation_timestamp": creation_timestamp,
        }

        env_dict = {
            "loader" :		FileSystemLoader("templates"),
            "autoescape" :	select_autoescape(['html', 'xml']),
            "trim_blocks" :	True,
            "lstrip_blocks":True,
        }
        env = Environment(**env_dict)
        
        template = env.get_template(template_name)
        response = template.render(**jinja_dict)
        with open(f"{weapon_label.lower()}_{gender_label.lower()}.html", "w+", encoding="utf-8") as file:
            file.write(response)


# Index page

template_name = "template_index.html"
jinja_dict = {
    "genders": genders,
    "weapons": weapons,
    "creation_timestamp": creation_timestamp,
}

env_dict = {
    "loader" :		FileSystemLoader("templates"),
    "autoescape" :	select_autoescape(['html', 'xml']),
    "trim_blocks" :	True,
    "lstrip_blocks":True,
}
env = Environment(**env_dict)

template = env.get_template(template_name)
response = template.render(**jinja_dict)
with open("index.html", "w+", encoding="utf-8") as file:
    file.write(response)

