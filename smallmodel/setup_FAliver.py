import pandas as pd
import libsbml as sbml
import cobra


def create_model(mets: pd.DataFrame, rxns: pd.DataFrame, p: pd.DataFrame):
    cobra_model = cobra.Model('SimpleFALiver')
    r = cobra_model.reactions
    # m = cobra_model.metabolites
    mets["cobra_mets"] = mets.apply(
        lambda x: cobra.Metabolite(
            x["id"],
            compartment=x["compartment"]
        ),
        axis=1
    )
    cobra_model.add_metabolites(mets["cobra_mets"])
    rxns["cobra_rxns"] = rxns.apply(
        lambda x: cobra.Reaction(
            x["id"]
        ),
        axis=1
    )
    cobra_model.add_reactions(rxns["cobra_rxns"])
    rxns.apply(
        lambda x:
            r.get_by_id(x["id"]).build_reaction_from_string(x["reaction"]),
        axis=1
    )
    cobra.io.write_sbml_model(cobra_model, 'SimpleFALiver.xml')

    # further edeit model in sbml:
    sbml_model = sbml.readSBML('SimpleFALiver.xml')
    mmole = sbml_model.getModel().createUnitDefinition()
    mmole.setId('mmole')
    unit = mmole.createUnit()
    unit.setKind(sbml.UNIT_KIND_MOLE)
    unit.setExponent(1)
    unit.setScale(-3)
    unit.setMultiplier(1)

    hr = sbml_model.getModel().createUnitDefinition()
    hr.setId('h')
    unit = hr.createUnit()
    unit.setKind(sbml.UNIT_KIND_SECOND)
    unit.setExponent(1)
    unit.setScale(0)
    unit.setMultiplier(3600)

    mMph = sbml_model.getModel().createUnitDefinition()
    mMph.setId('mmole_per_hour')
    unit = mMph.createUnit()
    unit.setKind(sbml.UNIT_KIND_MOLE)
    unit.setExponent(1)
    unit.setScale(-3)
    unit.setMultiplier(1)
    unit_1 = mMph.createUnit()
    unit_1.setKind(sbml.UNIT_KIND_SECOND)
    unit_1.setExponent(-1)
    unit_1.setScale(0)
    unit_1.setMultiplier(3600)

    for i, row in p.iterrows():
        param = sbml_model.getModel().createParameter()
        param.setId(row['id'])
        if row['id'][:2] == "vm":
            param.setValue(row['value']*10)
        else:
            param.setValue(row['value'])
        param.setUnits(row['unit'])
        param.setConstant(True)

    for i, row in rxns.iterrows():
        math_ast = sbml.parseL3Formula(row['rate'])
        kinetic_law = sbml_model.getModel().getReaction(
            "R_" + row['id']
        ).createKineticLaw()
        kinetic_law.setMath(math_ast)

    for i, row in mets.iterrows():
        met = sbml_model.getModel().getSpecies("M_" + row['id'])
        met.setInitialAmount(row['init'])
        met.setConstant(row['constant'])
        met.setBoundaryCondition(row['boundary'])
        met.setSubstanceUnits("mmole")

    rr = sbml_model.getModel().createRateRule()
    rr.setVariable("M_LD")

    return sbml.writeSBMLToString(sbml_model)


if __name__ == "__main__":
    mets = pd.read_csv("small_FA_mets.csv", skipinitialspace=True)
    rxns = pd.read_csv("small_FA_rxns.csv", skipinitialspace=True)
    p = pd.read_csv("small_FA_paras.csv", skipinitialspace=True)
    sbml_string = create_model(mets, rxns, p)
    with open("SimpleFALiver.xml", "w") as f:
        f.write(sbml_string)
