from . import engine
from concurrent.futures import ThreadPoolExecutor

def create(**options):
    model = engine.neuralNetworkModel(options.get("name"))
    model.layers = options.get("layers")
    model._init_weights()
    return model

def load(**options):
    model = engine.neuralNetworkModel(options.get("name"))
    model.load()
    return model

#Main backprop function with multithread support mini batch gradient descent
def mbgd(model, data_input, data_output, **options):

    #Get function parameters
    batch_size, epoch_number, learning_rate = options.get("batch_size"), options.get("epoch_number"), options.get("rate")

    #Function used to multithread each backprop of a batch inside the main backprop function
    def _backpropagate_batch(model, input, output, calculate_loss):
        run_history = model._run(input) #Run the model and save the history of each neuron output inside the network
        model._backpropagate(run_history, output, not(calculate_loss)) #Backprop over the network

    #Loop over each epoch
    for epoch in range(epoch_number):
        loss = 0 #initialize loss variable

        #Loop over the entire dataset, n-time where n is len(data)/batch_size, so an iteration for each batch
        for batch_start in range(0, len(data_input), batch_size): #batch_start is the index of the start of the batch
            batch_end =  min(batch_start + batch_size,len(data_input)) #batch_end is the index of the end of the batch
            model._init_batch() #Call init_batch() before running the backprop, initializes the space to store weights and biases modifications

            #Multithread each single run and backpropagation of a batch
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                for i in range(batch_start, batch_end): #Loop over each single input inside a batch
                    executor.submit(_backpropagate_batch, model, data_input[i], data_output[i], i-batch_start) #Call _backpropagate_batch() for each thread

            #extract the average loss of the batch (simulated average for speed optimization)
            loss += model.loss
            #Update weights and biases of the model based on the backpropagation
            model._update_weights(batch_size, learning_rate)

        #Print median loss for each epoch
        print("Epoch = " + str(epoch) + " Loss = " + str(loss/(len(data_input)/batch_size)), end='\r')

    #Save the model
    model.save()
    print("\nTraining finished, model saved.")
