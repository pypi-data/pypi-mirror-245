# Tests for the pyudcp module
import sys
import pyudcp.enigmapy as ep

sys.path.insert(0, '../src')
# import pyudcp as ep


def test_enigmapy():
    cli = ep.UDCPPythonBinding()
    cli.setExecutableRootDir("/Users/yogeshbarve/Projects/rest-tutorials/Pydantic-test/LEAP_CLI")
    cli.metadataModelCodeGen("e0de6a4a-5257-4f2c-b3ce-470e3299fc4a",
                             "./test",
                             "DigitalPhenotypingSchema.json",
                             "DigitalPhenotypingContentModel.py",
                             "DigitalPhenotypingContentModel")

def test_repo_listing():
    cli = ep.UDCPPythonBinding()
    cli.setExecutableRootDir("/Users/yogeshbarve/Projects/rest-tutorials/Pydantic-test/LEAP_CLI")
    cli.run_repo_listing()


def captureMetadataInfo():
    import sys
    # Specify the folder containing the generated pydantic model of the metadata
    sys.path.insert(0, './test')
    import DigitalPhenotypingContentModel as model
    mymodel = model.DigitalPhenotypingContentModel()
    mymodel.participant = model.Participant()
    mymodel.participant.participant = model.Participant1()
    mymodel.participant.participant.participant_id = "1234567890"
    mymodel.participant.participant.participant_status = model.Dropout(dropout={})
    generatedJSON = mymodel.model_dump_json(indent=2, by_alias=True, exclude_unset=False, exclude_none=True)
    return generatedJSON


def generateMetaDataJSONFile():
    import json
    tmpjson = {
        'taxonomyVersion': json.loads(open("./test/taxonomyVersion.json").read()),
        'taxonomyTags': [json.loads(captureMetadataInfo())]
    }
    return tmpjson

def testDownload():
    cli = ep.UDCPPythonBinding()
    cli.setExecutableRootDir("/Users/yogeshbarve/Projects/rest-tutorials/Pydantic-test/LEAP_CLI")
    # cli.run_repo_listing()
    cli.downloadData("./test", "pdp://leappremonitiondev.azurewebsites.net/sandbox_emav1/586370a0-0a42-4c02-a051-174095d894af/1/0")

def testUpload():
    cli = ep.UDCPPythonBinding()
    cli.setExecutableRootDir("/Users/yogeshbarve/Projects/rest-tutorials/Pydantic-test/LEAP_CLI")
    testmetadataGeneration("./test/metadataUpload.json")
    cli.uploadData("./upload", "ae0f62d0-854b-4696-8c7d-54e89e04308e", "./test/metadataUpload.json", "Testing Python CLI Upload")


def testmetadataGeneration(file_path: "./test/metadataUpload.json"):
    import json
    metadataUpload = json.dumps(generateMetaDataJSONFile(), indent=2)
    # Save the generated file
    with open(file_path, "w") as outfile:
        outfile.write(metadataUpload)
        outfile.close()


if __name__ == '__main__':
    # test_enigmapy()
    # testDownload()
    # test_repo_listing()
    # testDownload()
    # testUpload()



