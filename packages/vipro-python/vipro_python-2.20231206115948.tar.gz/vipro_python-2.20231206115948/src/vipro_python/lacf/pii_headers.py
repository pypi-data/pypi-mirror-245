import pandas

def break_out_individuals_cpl(
    df: pandas.DataFrame,
    header_map: dict, 
    additional_columns: list) -> pandas.DataFrame:
  """
  Variation: Complainant, Partner, Landlord.

  After receiving A.I. intelligence in the form of header_map, 
  we will rename the dataframe for you and break out the possible
  Complainant, Partner and Landlord individuals so the dataframe returned
  is one row per individual (with a row_type column added). 
  
  Some dataframes need additional columns for meta-data, which you can
  include too.

  We will not modify your dataframe passed into this function, making 
  it idempotent.
  """
  
  # rename pii columns
  renamed_df = df.rename(columns=header_map)

  # all possible columns we may need to include
  extras = additional_columns if additional_columns is not None else []
  claimant_columns = extras + ['unique_id', 'nino', 'surname', 'forename', 'date_of_birth', 'address_1', 'address_2', 'address_3', 'postcode']
  partner_columns = extras + ['unique_id', 'partner_nino', 'partner_surname', 'partner_forename', 'partner_date_of_birth', 'address_1', 'address_2', 'address_3', 'postcode']
  landlord_columns = extras + ['unique_id', 'landlord_nino', 'landlord_surname', 'landlord_forename', 'landlord_date_of_birth', 'landlord_address_1', 'landlord_address_2', 'landlord_address_3', 'landlord_postcode']

  # build our separate dataframes for each individual
  claimant_df = pandas.DataFrame(columns=claimant_columns)
  partner_df = pandas.DataFrame(columns=partner_columns)
  landlord_df = pandas.DataFrame(columns=landlord_columns)

  # extract relevant columns from the original dataframe
  claimant_df = renamed_df[[col for col in claimant_columns if col in renamed_df]].copy()
  partner_df = renamed_df[[col for col in partner_columns if col in renamed_df]].copy()
  landlord_df = renamed_df[[col for col in landlord_columns if col in renamed_df]].copy()

  # Rename columns to make them consistent
  partner_df = partner_df.rename(columns={ 'partner_nino': 'nino', 'partner_surname': 'surname', 'partner_forename': 'forename', 'partner_date_of_birth': 'date_of_birth' }, errors='ignore')
  landlord_df = landlord_df.rename(columns={ 'landlord_nino': 'nino', 'landlord_surname': 'surname', 'landlord_forename': 'forename', 'landlord_date_of_birth': 'date_of_birth', 'landlord_address_1': 'address_1', 'landlord_address_2': 'address_2', 'landlord_address_3': 'address_3', 'landlord_postcode': 'postcode' }, errors='ignore')

  # mark the differences
  claimant_df['row_type'] = 'claimant'
  partner_df['row_type']  = 'partner'
  landlord_df['row_type'] = 'landlord'

  # Concatenate the three dataframes into a single dataframe
  combined_df = pandas.concat([claimant_df, partner_df, landlord_df], axis=0, ignore_index=True) \
    .dropna(subset=['forename', 'surname', 'address_1', 'postcode'])

  # stats
  print(f"claimants: {len(claimant_df)}")
  print(f"partners: {len(partner_df)}")
  print(f"landlords: {len(landlord_df)}")
  print(f"final tally {len(combined_df)} valid residents")
  return combined_df