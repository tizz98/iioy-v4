import { h, component } from 'fpreact';
import classNames from 'classnames';
import { Input, Container } from 'mdbreact';
import { DebounceInput } from 'react-debounce-input';
import Title from '../../components/title';
import { COLORS } from '../../components/title-header';
import HeaderContainer from '../../components/title-header/container';
import MovieList from '../../components/movies/list';
import { BASE_URL } from '../../api';
import style from './style';

const initialModel = {
	searchTerm: '',
	previousTerm: '',
	searchActive: false,
	results: null,
};
const Msg = {
	setSearchTerm: 0,
	setSearchActive: 1,
	setSearchInactive: 2,
	getSearchResults: 3,
	setSearchResults: 4,
};
const searchMovies = query => (
	dispatch => (
		fetch(`${BASE_URL}movies/search/?q=${query}`)
		.then(res => res.json())
		.then(res => dispatch(Msg.setSearchResults)(res))
		.catch(err => dispatch(Msg.setSearchResults)(null, err))
	)
);
export default component({
	update(model = initialModel, msg) {
		switch (msg.kind) {
			case Msg.setSearchActive:
				return { ...model, searchActive: true };
			case Msg.setSearchInactive:
				return { ...model, searchActive: false };
			case Msg.setSearchTerm:
				const newSearchTerm = msg.value.target ? msg.value.target.value : msg.value;
				const newModel = {
					...model,
					searchTerm: newSearchTerm,
					previousTerm: model.searchTerm,
				};

				if (newModel.searchTerm !== newModel.previousTerm) {
					return [newModel, searchMovies(newModel.searchTerm)];
				}

				return newModel;
			case Msg.setSearchResults:
				return { ...model, results: msg.value };
		}

		return model;
	},

	view(model, dispatch) {
		console.log(model.searchTerm)
		return (
			<div class={style.home}>
				<Title />
				<HeaderContainer
					color={ COLORS.violet }
					height="500px"
				>
					<Container>
						<div className="md-form">
							<DebounceInput
								className="form-control"
								minLength={ 2 }
								debounceTimeout={ 300 }
								onChange={ dispatch(Msg.setSearchTerm) }
								onFocus={ dispatch(Msg.setSearchActive) }
								onBlur={ () => model.searchTerm ? null : dispatch(Msg.setSearchInactive)() }
							/>
							<label
								htmlFor="search"
								className={ classNames({
									active: model.searchActive,
									'white-text': !model.searchActive,
								}) }
							>
								{ model.searchTerm && !model.searchActive ? '' : 'Search'}
							</label>
						</div>
					</Container>
				</HeaderContainer>

				{
					model.results !== null &&
					<MovieList movies={ model.results } />
				}
			</div>
		);
	},
});
