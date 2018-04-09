import { h, component } from 'fpreact';
import { Router } from 'preact-router';

import Header from './header';
import Footer from './footer';
import Home from '../routes/home';
import About from '../routes/about';
import Movies from '../routes/movies';
import MovieList from '../routes/lists';
import Genre from '../routes/genres';
import Legal from '../routes/legal';

if (module.hot) {
	require('preact/debug');
}

const initialModel = {
	currentUrl: null,
};
const Msg = {
	updateUrl: 0,
};

const App = component({
	update(model = initialModel, msg) {
		switch (msg.kind) {
			case Msg.updateUrl:
				return { ...model, currentUrl: msg.value.url };
		}

		return model;
	},

	view(model, dispatch) {
		return (
			<div id="app">
				<Header />
				<Router onChange={ dispatch(Msg.updateUrl) }>
					<Home path="/" />
					<About path="/about" />
					<Legal path="/legal" />
					<Movies path="/movies/:id" />
					<Movies path="/movies/:id/:slug" />
					<MovieList path="/lists/:slug" />
					<Genre path="/genres/:id" />
				</Router>
				<Footer />
			</div>
		);
	},
});

export default App;
