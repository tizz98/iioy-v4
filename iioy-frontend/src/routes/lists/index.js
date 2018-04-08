import { h, component } from 'fpreact';
import { route } from 'preact-router';
import { Container } from 'mdbreact';
import Title from '../../components/title';
import TitleHeader from '../../components/title-header';
import MovieList from '../../components/movies/list';
import { BASE_URL } from '../../api';
import style from './style';

const initialModel = {
    slug: null,
    data: null,
    name: null,
    error: null,
};
const Msg = {
    setSlug: 0,
    setData: 1,
    getData: 2,
};

const getListData = slug => (
    dispatch => (
        fetch(`${BASE_URL}lists/${slug}/`)
        .then(res => res.json())
        .then(res => dispatch(Msg.setData)(res))
        .catch(err => dispatch(Msg.setData)(null, err))
    )
);

export default component({
    props({ matches }, dispatch) {
        dispatch(Msg.setSlug)(matches.slug);
        dispatch(Msg.getData)();
    },

    update(model = initialModel, msg) {
        switch (msg.kind) {
            case Msg.setSlug:
                return { ...model, slug: msg.value, name: msg.value };
            case Msg.setData:
                if (msg.error) {
                    return { ...model, error: msg.error };
                }
                return { ...model, data: msg.value, name: msg.value.name };
            case Msg.getData:
                return [model, getListData(model.slug)];
        }
        return model;
    },

    view({ slug, data, error, name }, dispatch) {
        return (
            <div className={ style.main }>
                <Title title={ name } />
                <TitleHeader text={ name } />
                <MovieList movies={ data && data.movies } />
            </div>
        );
    },
});
