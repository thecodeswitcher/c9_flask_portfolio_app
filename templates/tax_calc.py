filing_single = {
             0.10: {'lower':0, 'upper':9700}
            ,0.12: {'lower': 9701, 'upper': 39475}
            ,0.22: {'lower': 39476, 'upper': 84200}
            ,0.24: {'lower': 84201, 'upper': 160725}
            ,0.32: {'lower': 160726, 'upper': 204100}
            ,0.35: {'lower': 204101, 'upper': 510300}
            ,0.37: {'lower': 510301, 'upper':None}
              }

def tax_bracket_calc(income,tax_dict = filing_single, deduction =12200):

    taxable_income = income - deduction

    print("Taxable income {}".format(taxable_income))

    tax_owed = 0

    tax_owed_dict = tax_dict

    for bracket in tax_dict:

        bracket_lower = tax_dict[bracket]['lower']
        bracket_upper = tax_dict[bracket]['upper']

        if bracket_upper == None:

            bracket_upper = taxable_income

        if taxable_income < bracket_lower:

            break

        taxable_income_in_range = min(taxable_income, bracket_upper)-bracket_lower

        tax_owed += bracket* taxable_income_in_range

        tax_owed_dict[bracket]['tax_owed'] = bracket* taxable_income_in_range
        tax_owed_dict[bracket]['portion_income_taxed'] = taxable_income_in_range

    print("Total tax_owed: {}".format(tax_owed))

    print("Effective Tax Rate: {0:3.2f}%".format((tax_owed/income)*100))

    return tax_owed_dict