import { h, component } from 'fpreact';
import { BASE_URL } from '../../api';
import Title from '../../components/title';
import TitleHeader from '../../components/title-header';
import MovieList from '../../components/movies/list';
import style from './style';

const initialModel = {
    error: null,
    data: null,
    id: null,
    name: null,
};
const Msg = {
    setProps: 0,
    setData: 1,
    getData: 2,
};
const getGenreData = id => (
    dispatch => (
        fetch(`${BASE_URL}genres/${id}/`)
        .then(res => res.json())
        .then(res => dispatch(Msg.setData)(res))
        .catch(err => dispatch(Msg.setData)(null, err))
    )
);

export default component({
    props({ matches }, dispatch) {
        dispatch(Msg.setProps)({
            id: matches.id,
            data: null,
            error: null,
            movies: null,
        });
        dispatch(Msg.getData)();
    },

    update(model = initialModel, msg) {
        switch (msg.kind) {
            case Msg.setProps:
                return { ...model, ...msg.value };
            case Msg.setData:
                if (msg.error) {
                    return { ...model, error: msg.error };
                }
                return { ...model, data: msg.value, name: msg.value.name };
            case Msg.getData:
                return [model, getGenreData(model.id)];
        }

        return model;
    },

    view({ name, data }, dispatch) {
        return (
            <div className={ style.main }>
                <Title title={ name } />
                <TitleHeader text={ name } />
                <MovieList movies={ data && data.movies } />
            </div>
        );
    },
});
