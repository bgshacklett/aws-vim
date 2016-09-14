" Vim syntax file
" Language:     AWS CloudFormation Templates (cft)
" Last Change:  2016 Sept 14
"
" Maintainer:   Andrew Stuart <andrew.stuart2@gmail.com>

" Type definitions
syn match typeDec /"Type"\s*:\s*"*/  nextgroup=type containedin=ALL
syn match   type           /\(\w\|:\)\+/ contained

" Reference object
syn match   ref          /{\s*"Ref"\s*:\_.\{-}}/

" Functions and predefined AWS
syn match   fn     /Fn::\w\+/ containedin=ALL
syn match   predef   /AWS::\(\w\|:\)\+/ containedin=ALL

" "Keywords"
syn keyword Keyword containedin=ALL
      \ AWSTemplateFormatVersion
      \ ConstraintDescription
      \ NoEcho
      \ Type
      \ Ref
      \ Default
      \ Description
      \ MinLength
      \ MaxLength
      \ AllowedPattern
      \ AllowedValues
      \ Metadata
      \ Parameters
      \ Outputs
      \ Properties
      \ Label
      \ TemplateURL

hi def link ref Special
hi def link fn Function
hi def link predef Constant
hi def link type Type
