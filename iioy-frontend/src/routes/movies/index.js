import { h, component } from 'fpreact';
import { Container, Col, Row } from 'mdbreact';
import moment from 'moment';
import classNames from 'classnames';
import { formatMoney } from 'accounting-js';
import Title from '../../components/title';
import TitleHeader, { COLORS } from '../../components/title-header';
import MovieList from '../../components/movies/list';
import Bubble, { BubbleList } from '../../components/bubble';
import PosterImage from '../../components/movies/poster-image';
import Loader from '../../components/loader';
import Video from '../../components/video';
import Display from '../../components/display';
import { BASE_URL } from '../../api';
import style from './style';

const initialModel = {
    error: null,
    data: null,
    id: null,
    slug: null,
    title: null,
    isLoading: false,
};
const Msg = {
    setProps: 0,
    setData: 1,
    getData: 2,
};

const getMovieData = id => (
    dispatch => (
        fetch(`${BASE_URL}movies/${id}/`)
        .then(res => res.json())
        .then(res => dispatch(Msg.setData)(res))
        .catch(err => dispatch(Msg.setData)(null, err))
    )
);

const Header = ({ children }) => <h3 className="h3-responsive mt-3">{ children }</h3>;

const Movie = component({
    props({ matches }, dispatch) {
        dispatch(Msg.setProps)({
            id: matches.id,
            slug: matches.slug || '',
            title: matches.slug || '',
            data: null,
            error: null,
        });
        dispatch(Msg.getData)();
    },

    update(model = initialModel, msg) {
        switch (msg.kind) {
            case Msg.setProps:
                return { ...model, ...msg.value };
            case Msg.setData:
                if (msg.error) {
                    return { ...model, error: msg.error, isLoading: false };
                }
                return { ...model, data: msg.value, title: msg.value.title, isLoading: false };
            case Msg.getData:
                if (model.isLoading) {
                    return model;
                }

                return [{
                    ...model,
                    isLoading: true,
                }, getMovieData(model.id)];
        }

        return model;
    },

    view(model, dispatch) {
        const {
            error,
            data,
            id,
            slug,
            title,
            isLoading,
        } = model;

        const head = (
            <div>
                <Title title={ title } />
                <TitleHeader
                    text=""
                    height={ data ? data.backdrop_url ? "500px" : "300px" : "500px" }
                    color={ COLORS.blue }
                    backgroundImage={ data && data.backdrop_url }
                />
            </div>
        );

        if (isLoading) {
            return (
                <div className={ style.main }>
                    { head }
                    <Loader className="mt-3" />
                </div>
            )
        }

        const releaseDate = moment(data.release_date, 'YYYY-MM-DD');
        const hasSimilarMovies = data.similar_movies.length >= 6;

        return (
            <div className={ style.main }>
                { head }

                <Container>
                    <Row>
                        <Col xs="12" lg="4" xl="3">
                            <PosterImage
                                poster_url={ data.poster_url }
                                title={ data.title }
                                style={ { marginTop: '-250px' } }
                                maxWidth="100%"
                                className="hoverable img-fluid"
                            />
                        </Col>
                        <Col xs="12" lg="8" xl="9">
                            <div className={ style.movie_info }>
                                <h2 className="h2-responsive">{ data.title }</h2>
                                <p className="mb-2">{ releaseDate.format('LL') }</p>
                                {
                                    data.genres.map(genre => (
                                        <Bubble
                                            key={ genre.tmdb_id }
                                            href={ `/genres/${genre.tmdb_id}` }
                                            text={ genre.name }
                                        />
                                    ))
                                }
                            </div>
                        </Col>
                    </Row>

                    <Display when={ data.synopsis }>
                        <Header>Plot</Header>
                        <p>{ data.synopsis }</p>
                    </Display>

                    <Display when={ data.ratings && data.ratings.length > 0 }>
                        <Header>Ratings</Header>
                        <table className="table table-sm">
                            <thead>
                                <tr>
                                    <th>Source</th>
                                    <th>Rating</th>
                                </tr>
                            </thead>
                            <tbody>
                                {
                                    data.ratings.map(rating => (
                                        <tr key={ rating.source }>
                                            <td>{ rating.source }</td>
                                            <td>{ rating.value }</td>
                                        </tr>
                                    ))
                                }
                            </tbody>
                        </table>
                    </Display>

                    <Display when={ Boolean(data.trailer_url) }>
                        <Header>Trailer</Header>
                        <Video src={ data.trailer_url } />
                    </Display>

                    <Display when={ data.budget > 0 || data.revenue > 0 }>
                        <Header>Money</Header>
                        <table className="table table-sm">
                            <tbody>
                                {
                                    data.budget > 0 &&
                                    <tr>
                                        <td>Budget</td>
                                        <td>{ formatMoney(data.budget, { precision: 0 }) }</td>
                                    </tr>
                                }
                                {
                                    data.revenue > 0 &&
                                    <tr>
                                        <td>Revenue</td>
                                        <td>{ formatMoney(data.revenue, { precision: 0 }) }</td>
                                    </tr>
                                }
                            </tbody>
                        </table>
                    </Display>

                    <Display when={ hasSimilarMovies }>
                        <Header>Similar movies</Header>
                    </Display>
                </Container>

                <Display when={ hasSimilarMovies }>
                    <MovieList movies={ data.similar_movies.splice(0, 6) } maxWidth="150px" />
                </Display>
            </div>
        );
    },
});

export default Movie;
