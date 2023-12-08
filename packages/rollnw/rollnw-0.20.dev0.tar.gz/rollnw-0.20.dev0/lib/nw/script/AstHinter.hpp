#pragma once

#include "../log.hpp"
#include "Nss.hpp"

#include <vector>

namespace nw::script {

struct AstHinter : public BaseVisitor {
    AstHinter(Nss* parent, SourceRange range)
        : parent_{parent}
        , range_{range}
    {
    }

    virtual ~AstHinter() = default;

    Nss* parent_ = nullptr;
    SourceRange range_;
    std::vector<InlayHint> result_;

    const Declaration* locate_in_dependencies(const std::string& needle)
    {
        if (!parent_->is_command_script() && parent_->ctx()->command_script_) {
            auto sym = parent_->ctx()->command_script_->locate_export(needle, false);
            if (sym.decl) {
                return sym.decl;
            }
        }
        for (const auto it : parent_->ast().includes) {
            if (!it.script) { continue; }
            auto sym = it.script->locate_export(needle, false, true);
            if (sym.decl) {
                return sym.decl;
            }
        }
        return nullptr;
    }

    // -- Vistor
    virtual void visit(Ast* script)
    {
        for (auto decl : script->decls) {
            decl->accept(this);
        }
    }

    // Decls
    virtual void visit(FunctionDecl* decl)
    {
        // No op
    }

    virtual void visit(FunctionDefinition* decl)
    {
        decl->block->accept(this);
    }

    virtual void visit(StructDecl* decl)
    {
        // No op
    }

    virtual void visit(VarDecl* decl)
    {
        if (decl->init) { decl->init->accept(this); }
    }

    // Expressions
    virtual void visit(AssignExpression* expr)
    {
        expr->rhs->accept(this);
    }

    virtual void visit(BinaryExpression* expr)
    {
        expr->lhs->accept(this);
        expr->rhs->accept(this);
    }

    virtual void visit(CallExpression* expr)
    {
        if (contains_range(range_, expr->extent().range)) {
            std::string needle{expr->expr->var.loc.view()};
            auto exp = expr->expr->env.find(needle);
            const Declaration* decl = nullptr;
            if (exp && exp->decl) {
                decl = exp->decl;
            } else {
                decl = locate_in_dependencies(needle);
            }

            const FunctionDecl* fd = nullptr;
            if (auto d = dynamic_cast<const FunctionDecl*>(decl)) {
                fd = d;
            } else if (auto d = dynamic_cast<const FunctionDefinition*>(decl)) {
                fd = d->decl_inline;
            }
            if (!fd) { return; }

            size_t args = std::min(fd->params.size(), expr->args.size());
            for (size_t i = 0; i < args; ++i) {
                result_.push_back({fd->params[i]->identifier(), expr->args[i]->extent().range.start});
            }

            for (auto arg : expr->args) {
                arg->accept(this);
            }
        }
    }

    virtual void visit(ComparisonExpression* expr)
    {
        expr->lhs->accept(this);
        expr->rhs->accept(this);
    }

    virtual void visit(ConditionalExpression* expr)
    {
        expr->test->accept(this);
        expr->true_branch->accept(this);
        expr->false_branch->accept(this);
    }

    virtual void visit(DotExpression* expr)
    {
        expr->lhs->accept(this);
        expr->rhs->accept(this);
    }

    virtual void visit(GroupingExpression* expr)
    {
        if (expr->expr) { expr->expr->accept(this); }
    }

    virtual void visit(LiteralExpression* expr)
    {
        // No op
    }

    virtual void visit(LiteralVectorExpression* expr)
    {
        // No op
    }

    virtual void visit(LogicalExpression* expr)
    {
        expr->lhs->accept(this);
        expr->rhs->accept(this);
    }

    virtual void visit(PostfixExpression* expr)
    {
        expr->lhs->accept(this);
    }

    virtual void visit(UnaryExpression* expr)
    {
        expr->rhs->accept(this);
    }

    virtual void visit(VariableExpression* expr)
    {
        // No op
    }

    // Statements
    virtual void visit(BlockStatement* stmt)
    {
        for (auto decl : stmt->nodes) {
            decl->accept(this);
        }
    }

    virtual void visit(DeclList* stmt)
    {
        // No op
    }

    virtual void visit(DoStatement* stmt)
    {
        // No op
        stmt->expr->accept(this);
        stmt->block->accept(this);
    }

    virtual void visit(EmptyStatement* stmt)
    {
    }

    virtual void visit(ExprStatement* stmt)
    {
        stmt->expr->accept(this);
    }

    virtual void visit(IfStatement* stmt)
    {
        stmt->expr->accept(this);
        stmt->if_branch->accept(this);
        if (stmt->else_branch) {
            stmt->if_branch->accept(this);
        }
    }
    virtual void visit(ForStatement* stmt)
    {
        if (stmt->init) { stmt->init->accept(this); }
        if (stmt->check) { stmt->check->accept(this); }
        if (stmt->inc) { stmt->inc->accept(this); }
        stmt->block->accept(this);
    }

    virtual void visit(JumpStatement* stmt)
    {
        if (stmt->expr) { stmt->expr->accept(this); }
    }

    virtual void visit(LabelStatement* stmt)
    {
    }

    virtual void visit(SwitchStatement* stmt)
    {
        stmt->target->accept(this);
        stmt->block->accept(this);
    }

    virtual void visit(WhileStatement* stmt)
    {
        stmt->check->accept(this);
        stmt->block->accept(this);
    }
};

} // namespace nw::script
