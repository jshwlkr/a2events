/*global console require*/

var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var uncss = require('gulp-uncss');
var merge = require('merge-stream');

var input = './scss/**/*.scss';
var output = './';
var sassOptions = {
errLogToConsole: true,
outputStyle: 'expanded',
includePaths: 'node_modules/foundation-sites/scss'
};
var autoprefixerOptions = {
browsers: ['last 2 versions', '> 5%', 'Firefox ESR']
};

gulp.task('sass', function() {
  return gulp
    .src(input)
    .pipe(sass(sassOptions).on('error', sass.logError))
    .pipe(autoprefixer(autoprefixerOptions))
    .pipe(gulp.dest(output));
});

gulp.task('perf', function() {
  return gulp.src('main.css')
    .pipe(uncss({
    html: ['http://localhost:8000/']
    }))
    .pipe(gulp.dest('./'));
});

/*eslint no-console: 0*/
gulp.task('watch', function() {
  return gulp
    // Watch the input folder for change,
    // and run `sass` task when something happens
    .watch(input, ['sass'])
    // When there is a change,
    // log a message in the console
    .on('change', function(event) {
      console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
    });
});

gulp.task('default', ['sass', 'watch' /*, possible other tasks... */ ]);
