import { h, component } from 'fpreact';

const Movies = component({
    update(model, msg) {
        return model;
    },

    view(model, dispatch) {
        return (
            <div>
                <h1>movie!!</h1>
            </div>
        );
    },
});

export default Movies;
