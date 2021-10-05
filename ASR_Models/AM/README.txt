This model was trained with 11 following corpora:
--------------------------------------------------------------
| Corpus Name                |    Corpus Tyep       |  Hours  |
|-------------------------------------------------------------|
|Appen OTS US English ASR 001|    Reading           |  371    |
|-------------------------------------------------------------|
|Appen OTS US English ASR 002| Customer service call|   5     |
|-------------------------------------------------------------|
|Appen OTS US English ASR 003| Mobile Conversation  |  975    |
|-------------------------------------------------------------|
|Common Voice                |   Crowd sourcing     |  241    |
|-------------------------------------------------------------|
|VoxForge US English         |   Crowd sourcing     |   63    |
|-------------------------------------------------------------|
|TED-LIUM r1                 |    Public speech     |   118   |
|-------------------------------------------------------------|
|TED-LIUM r2                 |    Public speech     |   207   |
|-------------------------------------------------------------|
|TED-LIUM r3                 |    Public speech     |   452   |
|-------------------------------------------------------------|
|LibriSpeech                 |     Audio book       |   960   |
|-------------------------------------------------------------|
|Fisher                      | Conv. tel speech     |   2742  |
|-------------------------------------------------------------|
|Switchboard                 | Conv. tel speech     |   260   |
|-------------------------------------------------------------|
|Total                       |          -           |   6394  |
---------------------------------------------------------------
the model network is the chain model in kaldi scrip:
the orginal script generate the model in folder:
exp/chain_cleaned/tdnn_cnn_1a_sp_online
