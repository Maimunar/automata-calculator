set grammar_filename="Calculator"
set lexer_filename="LexerRules"
set grammar_start="main"
set java_env="java"

@echo off
echo "Deleting all files in java environment folder..."
del %java_env%\*.* /s /q
echo "Copying grammar file to java environment folder..."
copy %grammar_filename%.g4 %java_env%
copy %lexer_filename%.g4 %java_env%
cd %java_env%
call antlr4 %grammar_filename%.g4
echo "Compiling java files..."
javac %grammar_filename%*.java
set /p text_file="Please provide a relative path location to the text file you want to parse: "
call grun %grammar_filename% %grammar_start% < %text_file% -gui
cd ..