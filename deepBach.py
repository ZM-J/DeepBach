"""
@author: Gaetan Hadjeres
"""

import click

from DatasetManager.chorale_dataset import ChoraleDataset
from DatasetManager.dataset_manager import DatasetManager
from DatasetManager.metadata import FermataMetadata, TickMetadata, KeyMetadata

from DeepBach.model_manager import DeepBach

from choralefy import choralefy

@click.command()
@click.option('--note_embedding_dim', default=20,
              help='size of the note embeddings')
@click.option('--meta_embedding_dim', default=20,
              help='size of the metadata embeddings')
@click.option('--num_layers', default=2,
              help='number of layers of the LSTMs')
@click.option('--lstm_hidden_size', default=256,
              help='hidden size of the LSTMs')
@click.option('--dropout_lstm', default=0.5,
              help='amount of dropout between LSTM layers')
@click.option('--linear_hidden_size', default=256,
              help='hidden size of the Linear layers')
@click.option('--batch_size', default=256,
              help='training batch size')
@click.option('--num_epochs', default=5,
              help='number of training epochs')
@click.option('--train', is_flag=True,
              help='train the specified model for num_epochs')
@click.option('--num_iterations', default=2500,
              help='number of parallel pseudo-Gibbs sampling iterations')
@click.option('--sequence_length_ticks', default=64,
              help='length of the generated chorale (in ticks)')
@click.option('--input_midi', default='MyInput/chorale_7_soprano.mid',
              help='input midi for prediction')
def main(note_embedding_dim,
         meta_embedding_dim,
         num_layers,
         lstm_hidden_size,
         dropout_lstm,
         linear_hidden_size,
         batch_size,
         num_epochs,
         train,
         num_iterations,
         sequence_length_ticks,
         input_midi
         ):
    dataset_manager = DatasetManager()

    metadatas = [
       FermataMetadata(),
       TickMetadata(subdivision=4),
       KeyMetadata()
    ]
    chorale_dataset_kwargs = {
        'voice_ids':      [0, 1, 2, 3],
        'metadatas':      metadatas,
        'sequences_size': 8,
        'subdivision':    4
    }
    bach_chorales_dataset: ChoraleDataset = dataset_manager.get_dataset(
        name='bach_chorales',
        **chorale_dataset_kwargs
        )
    dataset = bach_chorales_dataset

    deepbach = DeepBach(
        dataset=dataset,
        note_embedding_dim=note_embedding_dim,
        meta_embedding_dim=meta_embedding_dim,
        num_layers=num_layers,
        lstm_hidden_size=lstm_hidden_size,
        dropout_lstm=dropout_lstm,
        linear_hidden_size=linear_hidden_size
    )

    if train:
        deepbach.train(batch_size=batch_size,
                       num_epochs=num_epochs)
    else:
        deepbach.load()
        deepbach.cuda()

    print('Generation')

    if (input_midi != ''):
        input_chorale = choralefy(input_midi)
        
        input_tensor = bach_chorales_dataset.get_score_tensor(input_chorale, 0., input_chorale.flat.highestTime)
        input_metadata = bach_chorales_dataset.get_metadata_tensor(input_chorale)

        score, tensor_chorale, tensor_metadata = deepbach.generation(
            num_iterations=num_iterations,
            tensor_chorale=input_tensor,
            tensor_metadata=input_metadata,
            sequence_length_ticks=sequence_length_ticks,
            random_init=True,
            voice_index_range=[1,2,3]
        )
    else:
        score, tensor_chorale, tensor_metadata = deepbach.generation(
            num_iterations=num_iterations,
            sequence_length_ticks=sequence_length_ticks,
        )
    score.show()


if __name__ == '__main__':
    main()
