var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('sass', function () {
  gulp.src('./sktimeline/static/scss/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./sktimeline/static/css'));
});

gulp.task('sass:watch', function () {
  gulp.watch('./sktimeline/static/scss/*.scss', ['sass']);
})
