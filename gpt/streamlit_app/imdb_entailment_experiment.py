import wandb
import streamlit as st


def imdb_text_entailment_app_module():
    from gpt.experiments.language_model import IMDBReviewLanguageExperiment
    experiment = IMDBReviewLanguageExperiment()
    initialize_wandb = st.checkbox('Initialize Wandb')

    if initialize_wandb:
        project_name = st.text_input('Wandb Project Name', 'gpt')
        experiment_name = st.text_input('Experiemnt Name', 'imdb_language_model')
        wandb_api_key = st.text_input('Wandb API Key', '')
        from gpt.experiments.utils import init_wandb
        st.text('Initializing Wandb...')
        init_wandb(
            project_name=project_name,
            experiment_name=experiment_name,
            wandb_api_key=wandb_api_key
        )
        wandb_url = str(wandb.run.url)
        st.markdown('<a href="{}">{}</a>'.format(wandb_url, wandb_url), unsafe_allow_html=True)
        st.text_input('Done!!!')

    st.text('Fetching and Building IMDB Large Movie Review Dataset...')
    experiment.build_dataset('https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz')
    st.text('Done!!!')

    start_text = st.text_input('Enter a start token to be infered upon during training', 'the actor was')
    st.text('Tokenizing Start Tokens...')
    start_tokens = experiment.tokenize(start_text=start_text)
    st.text('Done!!!')

    max_length = st.number_input('Enter max sequence length', 100)
    max_tokens = st.number_input('Enter max tokens to be predicted', 40)
    top_k = st.number_input('Enter number of top tokens to be sampled', 10)
    epochs = st.number_input('Enter number of epochs', 30)

    st.text('Training...')
    experiment.train(
        epochs=epochs, start_tokens=start_tokens,
        max_length=max_length, max_tokens=max_tokens,
        top_k=top_k, infer_every=1,
        log_on_wandb=True if initialize_wandb else False
    )
    st.text('Done!!!')
