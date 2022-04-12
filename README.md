# ksqlDB-test-session
Repo that will handle some basic and practical exercises with ksqlDB

### 1. Overview

The idea behind this repo, is to create a testing stage for ksqlDB. A .json file will be the center of attentions on this repo, and in it we can find four data dimensions: 1) `event_v2_data`, 2) `transaction`, 3) `transaction_request`, and 4) `payment_instrument_token_data`.

We will use these dimensions to "stream them" (since it will be a python function taking care of the emulation of this streaming procedure) into 4 different streams. From that, some transformation operations will be made and also some joins in order to reach to the desired subsets of data (these will be defined in the meantime).

### 2. ksqlDB

To this _testing stage_ we will use a Docker container with Kafka installed on it, and a python wrapper to the ksqlDB API, that will allow the interaction with this tool to be more familiar and easy for a person with some knowledge on python.

### 3. Dependencies

It is important to take care of the installation of the next modules:


